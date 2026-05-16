-- Pulizia per rendere lo script ri-eseguibile
TRUNCATE TABLE 
    dwh.bridge_event_weapon, 
    dwh.bridge_event_target, 
    dwh.fact_event, 
    dwh.dim_time, 
    dwh.dim_geography, 
    dwh.dim_group, 
    dwh.dim_attack_type, 
    dwh.dim_weapon, 
    dwh.dim_target 
RESTART IDENTITY CASCADE;

/*1. DIM_GEOGRAPHY*/
INSERT INTO dwh.dim_geography (geo_sk, city, provstate, country_name, region_name, latitude, longitude)
SELECT g.loc_id, g.city, g.provstate, c.country_name, r.region_name, g.latitude, g.longitude
FROM rd.geography g
JOIN rd.country c ON g.country_id = c.country_id
JOIN rd.region r ON c.region_id = r.region_id;

/* 2. DIM_GROUP*/
INSERT INTO dwh.dim_group (group_sk, gname, gsubname)
SELECT group_id, gname, gsubname FROM rd.terrorist_group;

/* 3. DIM_ATTACK_TYPE*/
INSERT INTO dwh.dim_attack_type (attack_sk, attack_name)
SELECT attacktype_id, attack_name FROM rd.attack_type;

/* 4. DIM_WEAPON*/
INSERT INTO dwh.dim_weapon (weapon_sk, weapon_name)
SELECT weaptype_id, weapon_name FROM rd.weapon;

/* 5. DIM_TARGET*/
INSERT INTO dwh.dim_target (target_sk, target_name)
SELECT targtype_id, target_name FROM rd.target;

/* 6. DIM_TIME*/
INSERT INTO dwh.dim_time (full_date, is_approximate_date, iyear, imonth, iday, quarter)
SELECT DISTINCT 
    full_date, is_approximate_date, iyear, imonth, iday,
    CASE 
        WHEN imonth BETWEEN 1 AND 3 THEN 1
        WHEN imonth BETWEEN 4 AND 6 THEN 2
        WHEN imonth BETWEEN 7 AND 9 THEN 3
        WHEN imonth BETWEEN 10 AND 12 THEN 4 
        ELSE NULL 
    END as quarter
FROM rd.event;

/* 7. FACT_EVENT (Aggiunto nkillter_reported)*/
INSERT INTO dwh.fact_event (eventid, date_sk, geo_sk, group_sk, attack_sk, nkill, nkillter, nwound, propvalue, nkillter_reported)
SELECT 
    e.eventid,
    t.date_sk,
    e.loc_id,
    e.group_id,
    e.attacktype_id,
    e.nkill,
    e.nkillter,
    e.nwound,
    e.propvalue,
    e.nkillter_reported
FROM rd.event e
JOIN dwh.dim_time t ON e.iyear = t.iyear AND e.imonth = t.imonth AND e.iday = t.iday;

/* 8. BRIDGE TABLES*/
INSERT INTO dwh.bridge_event_weapon (event_sk, weapon_sk)
SELECT f.event_sk, ew.weaptype_id
FROM rd.event_weapon ew
JOIN dwh.fact_event f ON ew.eventid = f.eventid;

INSERT INTO dwh.bridge_event_target (event_sk, target_sk)
SELECT f.event_sk, et.targtype_id
FROM rd.event_target et
JOIN dwh.fact_event f ON et.eventid = f.eventid;