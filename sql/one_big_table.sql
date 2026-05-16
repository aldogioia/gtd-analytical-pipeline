SELECT 
    f.eventid,
    f.nkill,
    f.nkillter,
    f.nwound,
    f.propvalue,
    f.nkillter_reported,
    t.full_date,
    t.is_approximate_date,
    t.iyear,
    t.quarter,
    t.imonth,
    t.iday,
    g.city,
    g.provstate,
    g.country_name,
    g.region_name,
    g.latitude,
    g.longitude,
    grp.gname AS terrorist_group,
    a.attack_name,
    w.weapon_name,
    tgt.target_name
FROM dwh.fact_event f
JOIN dwh.dim_time t ON f.date_sk = t.date_sk
JOIN dwh.dim_geography g ON f.geo_sk = g.geo_sk
JOIN dwh.dim_group grp ON f.group_sk = grp.group_sk
JOIN dwh.dim_attack_type a ON f.attack_sk = a.attack_sk
LEFT JOIN dwh.bridge_event_weapon bew ON f.event_sk = bew.event_sk
LEFT JOIN dwh.dim_weapon w ON bew.weapon_sk = w.weapon_sk
LEFT JOIN dwh.bridge_event_target bet ON f.event_sk = bet.event_sk
LEFT JOIN dwh.dim_target tgt ON bet.target_sk = tgt.target_sk;