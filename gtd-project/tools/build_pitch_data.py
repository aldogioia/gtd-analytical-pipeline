from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dataset" / "dwh_export"
OUTPUT = ROOT / "output" / "analysis" / "pitch_data.json"


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name, sep=";", decimal=",", low_memory=False)


fact = read("fact_event.csv")
time = read("dim_time.csv")[["date_sk", "iyear", "decade"]]
geo = read("dim_geography.csv")[["geo_sk", "country_name", "region_name"]]
groups = read("dim_group.csv")[["group_sk", "gname", "is_unknown_perpetrator"]]
attacks = read("dim_attack_type.csv")[["attack_sk", "attack_name", "attack_macro"]]
quality = read("dim_quality.csv")[["quality_sk", "date_accuracy", "nkill_source", "nwound_source"]]
weapons = read("dim_weapon.csv")[["weapon_sk", "weapon_name", "weapon_macro"]]
targets = read("dim_target.csv")[["target_sk", "target_name", "target_macro"]]
bridge_weapon = read("bridge_event_weapon.csv")
bridge_target = read("bridge_event_target.csv")

assert len(fact) == 209_706
assert int(fact["nkill"].sum()) == 523_944
assert bridge_weapon.loc[bridge_weapon["is_primary"], "event_sk"].nunique() == len(fact)
assert bridge_target.loc[bridge_target["is_primary"], "event_sk"].nunique() == len(fact)

base = (
    fact.merge(time, on="date_sk", how="left")
    .merge(geo, on="geo_sk", how="left")
    .merge(groups, on="group_sk", how="left")
    .merge(attacks, on="attack_sk", how="left")
    .merge(quality, on="quality_sk", how="left")
)

primary_weapons = bridge_weapon[bridge_weapon["is_primary"]].merge(weapons, on="weapon_sk", how="left")
primary_targets = bridge_target[bridge_target["is_primary"]].merge(targets, on="target_sk", how="left")
base = base.merge(primary_weapons[["event_sk", "weapon_name", "weapon_macro"]], on="event_sk", how="left")
base = base.merge(primary_targets[["event_sk", "target_name", "target_macro"]], on="event_sk", how="left")


def records(df: pd.DataFrame, columns: list[str]) -> list[dict]:
    clean = df[columns].copy()
    for col in clean.columns:
        if pd.api.types.is_float_dtype(clean[col]):
            clean[col] = clean[col].round(4)
    return clean.to_dict(orient="records")


yearly = (
    base.groupby("iyear", as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
    .query("iyear >= 1970 and iyear <= 2020")
)

decades = (
    base.groupby("decade", as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
    .query("decade != 'Unknown'")
)

suicide = (
    base.groupby("is_suicide", as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
)
suicide["lethality"] = suicide["deaths"] / suicide["events"]

targets_macro = (
    base.groupby("target_macro", as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
)
targets_macro["lethality"] = targets_macro["deaths"] / targets_macro["events"]
targets_macro = targets_macro.sort_values("events", ascending=False)

targets_detail = (
    base.groupby(["target_name", "target_macro"], as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
)
targets_detail["lethality"] = targets_detail["deaths"] / targets_detail["events"]

known_groups = base[~base["is_unknown_perpetrator"].fillna(True).astype(bool)]
top_groups = (
    known_groups.groupby("gname", as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
)
top_groups["lethality"] = top_groups["deaths"] / top_groups["events"]
top_groups = top_groups.sort_values("events", ascending=False).head(10)

source_counts = (
    base.groupby("nkill_source", as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
    .sort_values("events", ascending=False)
)

region_all = base.groupby("region_name", as_index=False).agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
region_all["lethality_all"] = region_all["deaths"] / region_all["events"]
region_reported = (
    base[base["nkill_source"] == "Reported"]
    .groupby("region_name", as_index=False)
    .agg(reported_events=("eventid", "nunique"), reported_deaths=("nkill", "sum"))
)
region_robustness = region_all.merge(region_reported, on="region_name", how="left")
region_robustness["lethality_reported"] = region_robustness["reported_deaths"] / region_robustness["reported_events"]
region_robustness["delta"] = (
    region_robustness["lethality_all"] - region_robustness["lethality_reported"]
) / region_robustness["lethality_reported"]
region_robustness = region_robustness.sort_values("delta", ascending=False)

weapon_target = (
    base.groupby(["target_macro", "weapon_macro"], as_index=False)
    .agg(events=("eventid", "nunique"), deaths=("nkill", "sum"))
)
weapon_target["lethality"] = weapon_target["deaths"] / weapon_target["events"]

unknown_share = float(base["is_unknown_perpetrator"].fillna(True).astype(bool).mean())
imputed_events = int((base["nkill_source"] == "Imputed").sum())

payload = {
    "totals": {
        "events": int(base["eventid"].nunique()),
        "deaths": int(base["nkill"].sum()),
        "lethality": float(base["nkill"].sum() / base["eventid"].nunique()),
        "unknown_share": unknown_share,
        "imputed_events": imputed_events,
        "imputed_share": imputed_events / base["eventid"].nunique(),
    },
    "yearly": records(yearly, ["iyear", "events", "deaths"]),
    "decades": records(decades, ["decade", "events", "deaths"]),
    "suicide": records(suicide, ["is_suicide", "events", "deaths", "lethality"]),
    "target_macro": records(targets_macro, ["target_macro", "events", "deaths", "lethality"]),
    "target_detail": records(targets_detail, ["target_name", "target_macro", "events", "deaths", "lethality"]),
    "top_groups": records(top_groups, ["gname", "events", "deaths", "lethality"]),
    "source_counts": records(source_counts, ["nkill_source", "events", "deaths"]),
    "region_robustness": records(
        region_robustness,
        ["region_name", "events", "lethality_all", "lethality_reported", "delta"],
    ),
    "weapon_target": records(weapon_target, ["target_macro", "weapon_macro", "events", "lethality"]),
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(OUTPUT)
print(json.dumps(payload["totals"], ensure_ascii=False, indent=2))
