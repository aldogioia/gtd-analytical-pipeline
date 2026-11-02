/*
   FASE 2 - PROCESSO ETL
   schema rd (reconciled)  ->  schema dwh (star schema)
*/

TRUNCATE TABLE
    dwh.bridge_event_weapon, dwh.bridge_event_target, dwh.fact_event,
    dwh.dim_time, dwh.dim_geography, dwh.dim_country, dwh.dim_group,
    dwh.dim_attack_type, dwh.dim_weapon, dwh.dim_target, dwh.dim_quality
RESTART IDENTITY CASCADE;



INSERT INTO dwh.dim_time
    (date_sk, full_date, iyear, decade, quarter, imonth, month_name, iday, day_of_week, day_name, is_weekend)
VALUES
    (-1, NULL, -1, 'Unknown', NULL, NULL, 'Unknown', NULL, NULL, 'Unknown', NULL);

/* 1.2 Calendario denso sull'intero intervallo osservato.
   Chiave surrogata YYYYMMDD, derivata dalla data stessa. Generando tutte
   le date, gli anni privi di attentati restano visibili invece di essere
   interpolati: e' cosi' che si riconosce il buco del 1993. */
INSERT INTO dwh.dim_time
    (date_sk, full_date, iyear, decade, quarter, imonth, month_name, iday, day_of_week, day_name, is_weekend)
SELECT
    CAST(TO_CHAR(cal.d, 'YYYYMMDD') AS INT),
    CAST(cal.d AS DATE),
    CAST(EXTRACT(YEAR FROM cal.d) AS INT),
    CAST(CAST(EXTRACT(YEAR FROM cal.d) AS INT) / 10 * 10 AS VARCHAR) || 's',
    CAST(EXTRACT(QUARTER FROM cal.d) AS SMALLINT),
    CAST(EXTRACT(MONTH FROM cal.d) AS SMALLINT),
    TRIM(TO_CHAR(cal.d, 'Month')),
    CAST(EXTRACT(DAY FROM cal.d) AS SMALLINT),
    CAST(EXTRACT(ISODOW FROM cal.d) AS SMALLINT),
    TRIM(TO_CHAR(cal.d, 'Day')),
    EXTRACT(ISODOW FROM cal.d) >= 6
FROM generate_series(
        (SELECT MAKE_DATE(CAST(MIN(iyear) AS INT), 1, 1)   FROM rd.event),
        (SELECT MAKE_DATE(CAST(MAX(iyear) AS INT), 12, 31) FROM rd.event),
        INTERVAL '1 day'
     ) AS cal(d);


INSERT INTO dwh.dim_country (country_sk, country_nk, country_name, region_name)
VALUES (-1, -1, 'Unknown', 'Unknown');

INSERT INTO dwh.dim_country (country_nk, country_name, region_name)
SELECT c.country_id, c.country_name, r.region_name
FROM rd.country c
JOIN rd.region r ON r.region_id = c.region_id
WHERE c.country_id <> -1;


INSERT INTO dwh.dim_geography
    (geo_sk, loc_nk, city, provstate, country_name, region_name, lat_centroid, lon_centroid)
VALUES
    (-1, -1, 'Unknown', 'Unknown', 'Unknown', 'Unknown', NULL, NULL);

INSERT INTO dwh.dim_geography
    (loc_nk, city, provstate, country_name, region_name, lat_centroid, lon_centroid)
SELECT g.loc_id, g.city, g.provstate, c.country_name, r.region_name,
       g.lat_centroid, g.lon_centroid
FROM rd.geography g
JOIN rd.country c ON c.country_id = g.country_id
JOIN rd.region  r ON r.region_id  = c.region_id;


INSERT INTO dwh.dim_group (group_sk, group_nk, gname, gsubname, is_unknown_perpetrator)
VALUES (-1, -1, 'Unknown', '', TRUE);

INSERT INTO dwh.dim_group (group_nk, gname, gsubname, is_unknown_perpetrator)
SELECT tg.group_id, tg.gname, tg.gsubname,
       tg.gname = 'Unknown'
FROM rd.terrorist_group tg;


INSERT INTO dwh.dim_attack_type (attack_sk, attack_nk, attack_name, attack_macro)
VALUES (-1, -1, 'Unknown', 'Unknown');

INSERT INTO dwh.dim_attack_type (attack_nk, attack_name, attack_macro)
SELECT at.attacktype_id, at.attack_name, at.attack_macro
FROM rd.attack_type at
WHERE at.attacktype_id <> -1;

INSERT INTO dwh.dim_weapon (weapon_sk, weapon_nk, weapon_subtype, weapon_name, weapon_macro)
VALUES (-1, -1, 'Unknown', 'Unknown', 'Unknown');

INSERT INTO dwh.dim_weapon (weapon_nk, weapon_subtype, weapon_name, weapon_macro)
SELECT ws.weapsubtype_id, ws.weapon_subtype_name, wt.weapon_name, wt.weapon_macro
FROM rd.weapon_subtype ws
JOIN rd.weapon_type wt ON wt.weaptype_id = ws.weaptype_id
WHERE ws.weapsubtype_id <> -1;

INSERT INTO dwh.dim_target (target_sk, target_nk, target_subtype, target_name, target_macro)
VALUES (-1, -1, 'Unknown', 'Unknown', 'Unknown');

INSERT INTO dwh.dim_target (target_nk, target_subtype, target_name, target_macro)
SELECT ts.targsubtype_id, ts.target_subtype_name, tt.target_name, tt.target_macro
FROM rd.target_subtype ts
JOIN rd.target_type tt ON tt.targtype_id = ts.targtype_id
WHERE ts.targsubtype_id <> -1;


INSERT INTO dwh.dim_quality
    (quality_sk, date_accuracy, nkill_source, nwound_source, perp_fatalities_source,
     claim_of_responsibility, perpetrator_attribution, doubt_terrorism, inclusion_criteria)
VALUES
    (-1, 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown');

INSERT INTO dwh.dim_quality
    (date_accuracy, nkill_source, nwound_source, perp_fatalities_source,
     claim_of_responsibility, perpetrator_attribution, doubt_terrorism, inclusion_criteria)
SELECT DISTINCT
    CASE WHEN e.is_approximate_date THEN 'Approximate' ELSE 'Exact' END,
    CASE WHEN e.is_nkill_imputed    THEN 'Imputed'     ELSE 'Reported' END,
    /* nwound non viene imputato: la provenance si legge dal NULL della misura.
       Etichettarlo 'Reported' quando e' assente renderebbe falsa la dimensione
       di qualita', che e' proprio cio' che deve impedire.                     */
    CASE WHEN e.nwound IS NULL      THEN 'Not Reported' ELSE 'Reported' END,
    CASE WHEN e.nkillter_reported   THEN 'Reported'    ELSE 'Not Reported' END,
    CASE WHEN e.claimed IS NULL THEN 'Unknown' WHEN e.claimed THEN 'Yes' ELSE 'No' END,
    CASE WHEN e.guncertain1 IS NULL THEN 'Unknown' WHEN e.guncertain1 THEN 'Suspected' ELSE 'Confirmed' END,
    CASE WHEN e.doubtterr IS NULL THEN 'Unknown' WHEN e.doubtterr THEN 'Yes' ELSE 'No' END,
    CASE WHEN e.crit1 IS NULL OR e.crit2 IS NULL OR e.crit3 IS NULL THEN 'Unknown'
         WHEN e.crit1 AND e.crit2 AND e.crit3 THEN 'All Three'
         ELSE 'Partial' END
FROM rd.event e;


WITH ev_quality AS (
    SELECT e.eventid,
        CASE WHEN e.is_approximate_date THEN 'Approximate' ELSE 'Exact' END AS date_accuracy,
        CASE WHEN e.is_nkill_imputed    THEN 'Imputed'     ELSE 'Reported' END AS nkill_source,
        CASE WHEN e.nwound IS NULL      THEN 'Not Reported' ELSE 'Reported' END AS nwound_source,
        CASE WHEN e.nkillter_reported   THEN 'Reported'    ELSE 'Not Reported' END AS perp_fatalities_source,
        CASE WHEN e.claimed IS NULL THEN 'Unknown' WHEN e.claimed THEN 'Yes' ELSE 'No' END AS claim_of_responsibility,
        CASE WHEN e.guncertain1 IS NULL THEN 'Unknown' WHEN e.guncertain1 THEN 'Suspected' ELSE 'Confirmed' END AS perpetrator_attribution,
        CASE WHEN e.doubtterr IS NULL THEN 'Unknown' WHEN e.doubtterr THEN 'Yes' ELSE 'No' END AS doubt_terrorism,
        CASE WHEN e.crit1 IS NULL OR e.crit2 IS NULL OR e.crit3 IS NULL THEN 'Unknown'
             WHEN e.crit1 AND e.crit2 AND e.crit3 THEN 'All Three'
             ELSE 'Partial' END AS inclusion_criteria
    FROM rd.event e
),
weapon_card AS (
    SELECT ew.eventid, COUNT(*) AS n FROM rd.event_weapon ew GROUP BY ew.eventid
),
target_card AS (
    SELECT et.eventid, COUNT(*) AS n FROM rd.event_target et GROUP BY et.eventid
)
INSERT INTO dwh.fact_event (
    eventid, date_sk, geo_sk, attack_country_sk, target_nat_sk,
    group_sk, attack_sk, quality_sk,
    latitude, longitude,
    nkill, nkillter, nwound, nperps, propvalue,
    is_success, is_suicide, is_extended, is_multiple, is_transnational,
    n_weapon_types, n_target_types
)
SELECT
    e.eventid,
    COALESCE(dt.date_sk, -1),
    COALESCE(dg.geo_sk, -1),
    COALESCE(dc.country_sk, -1),
    COALESCE(dn.country_sk, -1),
    COALESCE(dgr.group_sk, -1),
    COALESCE(da.attack_sk, -1),
    COALESCE(dq.quality_sk, -1),

    e.latitude,
    e.longitude,

    e.nkill,
    e.nkillter,
    e.nwound,
    e.nperps,
    e.propvalue,

    CASE WHEN e.success  THEN 1 WHEN NOT e.success  THEN 0 END,
    CASE WHEN e.suicide  THEN 1 WHEN NOT e.suicide  THEN 0 END,
    CASE WHEN e.extended THEN 1 WHEN NOT e.extended THEN 0 END,
    CASE WHEN e.multiple THEN 1 WHEN NOT e.multiple THEN 0 END,
    CASE WHEN e.natlty_id = -1 THEN NULL
         WHEN e.natlty_id <> rg.country_id THEN 1
         ELSE 0 END,

    CAST(COALESCE(wc.n, 0) AS SMALLINT),
    CAST(COALESCE(tc.n, 0) AS SMALLINT)

FROM rd.event e
JOIN rd.geography rg ON rg.loc_id = e.loc_id
LEFT JOIN dwh.dim_time        dt  ON dt.full_date  = e.full_date
LEFT JOIN dwh.dim_geography   dg  ON dg.loc_nk     = e.loc_id
LEFT JOIN dwh.dim_country     dc  ON dc.country_nk = rg.country_id
LEFT JOIN dwh.dim_country     dn  ON dn.country_nk = e.natlty_id
LEFT JOIN dwh.dim_group       dgr ON dgr.group_nk  = e.group_id
LEFT JOIN dwh.dim_attack_type da  ON da.attack_nk  = e.attacktype_id
LEFT JOIN ev_quality          vq  ON vq.eventid    = e.eventid
LEFT JOIN dwh.dim_quality     dq
       ON dq.date_accuracy           = vq.date_accuracy
      AND dq.nkill_source            = vq.nkill_source
      AND dq.nwound_source           = vq.nwound_source
      AND dq.perp_fatalities_source  = vq.perp_fatalities_source
      AND dq.claim_of_responsibility = vq.claim_of_responsibility
      AND dq.perpetrator_attribution = vq.perpetrator_attribution
      AND dq.doubt_terrorism         = vq.doubt_terrorism
      AND dq.inclusion_criteria      = vq.inclusion_criteria
LEFT JOIN weapon_card wc ON wc.eventid = e.eventid
LEFT JOIN target_card tc ON tc.eventid = e.eventid;


WITH weapon_arc AS (
    SELECT f.event_sk,
           dw.weapon_sk,
           ROW_NUMBER() OVER (PARTITION BY f.event_sk
                              ORDER BY ew.weap_order, dw.weapon_sk) AS arc_rank
    FROM rd.event_weapon ew
    JOIN dwh.fact_event  f  ON f.eventid    = ew.eventid
    JOIN dwh.dim_weapon  dw ON dw.weapon_nk = ew.weapsubtype_id
)
INSERT INTO dwh.bridge_event_weapon (event_sk, weapon_sk, is_primary)
SELECT event_sk, weapon_sk, arc_rank = 1
FROM weapon_arc;

WITH target_arc AS (
    SELECT f.event_sk,
           dt.target_sk,
           ROW_NUMBER() OVER (PARTITION BY f.event_sk
                              ORDER BY et.targ_order, dt.target_sk) AS arc_rank
    FROM rd.event_target et
    JOIN dwh.fact_event  f  ON f.eventid    = et.eventid
    JOIN dwh.dim_target  dt ON dt.target_nk = et.targsubtype_id
)
INSERT INTO dwh.bridge_event_target (event_sk, target_sk, is_primary)
SELECT event_sk, target_sk, arc_rank = 1
FROM target_arc;


INSERT INTO dwh.bridge_event_weapon (event_sk, weapon_sk, is_primary)
SELECT f.event_sk, -1, TRUE
FROM dwh.fact_event f
WHERE NOT EXISTS (SELECT 1 FROM dwh.bridge_event_weapon b WHERE b.event_sk = f.event_sk);

INSERT INTO dwh.bridge_event_target (event_sk, target_sk, is_primary)
SELECT f.event_sk, -1, TRUE
FROM dwh.fact_event f
WHERE NOT EXISTS (SELECT 1 FROM dwh.bridge_event_target b WHERE b.event_sk = f.event_sk);

UPDATE dwh.fact_event f
SET n_weapon_types = GREATEST(f.n_weapon_types, 1),
    n_target_types = GREATEST(f.n_target_types, 1);
