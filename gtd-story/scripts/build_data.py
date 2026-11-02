"""Rebuild website aggregates from the project's reconciled warehouse exports."""
from pathlib import Path
import json
import pandas as pd
PROJECT=Path(__file__).resolve().parents[1]
ROOT=PROJECT.parent
SRC=ROOT/'gtd-project/dataset/dwh_export'
OUT=PROJECT/'public/data'
def read(name): return pd.read_csv(SRC/(name+'.csv'),sep=';',decimal=',',low_memory=False)
f=read('fact_event')
for table,key,cols in [('dim_time','date_sk',['iyear']),('dim_group','group_sk',['gname','is_unknown_perpetrator']),('dim_attack_type','attack_sk',['attack_name']),('dim_quality','quality_sk',['nkill_source']),('dim_country','attack_country_sk',['country_name'])]:
    d=read(table)
    if table=='dim_country': d=d.rename(columns={'country_sk':key})
    f=f.merge(d[[key]+cols],on=key,validate='many_to_one')
for noun in ['weapon','target']:
    b=read('bridge_event_'+noun); b=b[b.is_primary]
    assert b.event_sk.nunique()==len(f)==len(b)
    b=b.merge(read('dim_'+noun),on=noun+'_sk')
    f=f.merge(b[['event_sk',noun+'_name',noun+'_macro']],on='event_sk',validate='one_to_one')
assert len(f)==209706 and int(f.nkill.sum())==523944
# The exported time dimension omits 2020-12-31. Recover only the year from
# the original source using eventid, without deriving dates from the identifier.
missing_year=~f.iyear.between(1970,2020)
time_recovered=int(missing_year.sum())
raw_year=pd.read_parquet(ROOT/'gtd-project/dataset/gtd_raw.parquet',columns=['eventid','iyear']).set_index('eventid').iyear
assert raw_year.index.is_unique
f.loc[missing_year,'iyear']=f.loc[missing_year,'eventid'].map(raw_year)
assert f.iyear.between(1970,2020).all()
f['iyear']=f.iyear.astype(int)

def stats(df,key):
    a=df.groupby(key,dropna=False).agg(events=('eventid','size'),deaths=('nkill','sum')).reset_index()
    a['lethality']=(a.deaths/a.events).round(3)
    return a.sort_values('events',ascending=False)
def records(df): return json.loads(df.to_json(orient='records'))
known=f[~f.is_unknown_perpetrator]
top=stats(known,'gname').head(10)
groups=[]
for row in records(top):
    row['weapons']=records(stats(f[f.gname==row['gname']],'weapon_name'))
    row['weaponMacros']=records(stats(f[f.gname==row['gname']],'weapon_macro'))
    groups.append(row)
years=[]
for y in range(1970,2021):
    sub=f[f.iyear==y]
    valid=sub[sub.is_transnational.isin([0,1])]
    years.append({'year':y,'events':len(sub) if y!=1993 else None,'deaths':int(sub.nkill.sum()) if y!=1993 else None,'suicide':int(sub.is_suicide.sum()),'transnational':round(float(valid.is_transnational.mean()*100),2) if len(valid) else None,'countries':records(stats(sub,'country_name').head(5))})
valid=f[f.is_transnational.isin([0,1])]
data={'totals':{'timeRecoveredEvents':time_recovered,'events':len(f),'deaths':int(f.nkill.sum()),'unknownShare':round(float(f.is_unknown_perpetrator.mean()*100),2),'transnationalShare':round(float(valid.is_transnational.mean()*100),2),'transnationalDenominator':len(valid),'knownGroups':int(known.gname.nunique()),'top10Share':round(float(top.events.sum()/len(known)*100),1),'imputedEvents':int((f.nkill_source=='Imputed').sum()),'reportedDeaths':int(f.loc[f.nkill_source=='Reported','nkill'].sum())},'years':years,'groups':groups,'attacks':{},'targets':{},'suicide':records(stats(f,'is_suicide')),'sources':records(stats(f,'nkill_source'))}
for mode in ['all','suicide']:
    sub=f if mode=='all' else f[f.is_suicide==1]
    data['attacks'][mode]=records(stats(sub,'attack_name'))
    # Macrocategories are those actually assigned by the project ETL.
    data['targets'][mode]=records(stats(sub,'target_macro'))
geo=f[f.latitude.between(-90,90)&f.longitude.between(-180,180)].copy()
geo['lat']=geo.latitude.round(2); geo['lng']=geo.longitude.round(2)
g=geo.groupby(['iyear','lat','lng'],sort=True).agg(n=('eventid','size'),deaths=('nkill','sum')).reset_index()
points={str(int(y)):[[r.lat,r.lng,int(r.n),int(r.deaths)] for r in part.itertuples()] for y,part in g.groupby('iyear')}
data['totals']['geocodedEvents']=len(geo)
data['totals']['geocodedDeaths']=int(geo.nkill.sum())
geo['lat_cell']=(geo.latitude//2).astype(int); geo['lng_cell']=(geo.longitude//2).astype(int)
cells=geo.groupby(['iyear','lat_cell','lng_cell']).agg(lat=('latitude','mean'),lng=('longitude','mean'),n=('eventid','size'),deaths=('nkill','sum')).reset_index()
map_points={str(int(y)):[[round(r.lat,4),round(r.lng,4),int(r.n),int(r.deaths)] for r in part.itertuples()] for y,part in cells.groupby('iyear')}

OUT.mkdir(parents=True,exist_ok=True)
(OUT/'story.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
(OUT/'locations.json').write_text(json.dumps(points,separators=(',',':')))
(OUT/'map-locations.json').write_text(json.dumps(map_points,separators=(',',':')))
print(json.dumps(data['totals'],indent=2)); print(top.to_string(index=False)); print(data['attacks']['all']); print(data['targets']['all'])
