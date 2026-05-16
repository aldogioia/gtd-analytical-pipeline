-- Pulizia per rendere lo script ri-eseguibile
TRUNCATE TABLE 
    rd.event_target,
    rd.event_weapon,
    rd.event,
    rd.terrorist_group,
    rd.geography,
    rd.country,
    rd.target,
    rd.weapon,
    rd.attack_type,
    rd.region
RESTART IDENTITY CASCADE;

-- 1. Tabelle Dimensionali di Lookup
INSERT INTO rd.region (region_id, region_name)
SELECT DISTINCT region, region_txt FROM staging.raw_gtd WHERE region IS NOT NULL;

INSERT INTO rd.attack_type (attacktype_id, attack_name)
SELECT DISTINCT attacktype1, attacktype1_txt FROM staging.raw_gtd WHERE attacktype1 IS NOT NULL;

INSERT INTO rd.weapon (weaptype_id, weapon_name)
SELECT DISTINCT weaptype1, weaptype1_txt FROM staging.raw_gtd WHERE weaptype1 IS NOT NULL;

INSERT INTO rd.target (targtype_id, target_name)
SELECT DISTINCT targtype1, targtype1_txt FROM staging.raw_gtd WHERE targtype1 IS NOT NULL;

-- 2. Country
INSERT INTO rd.country (country_id, country_name, region_id)
SELECT DISTINCT country, country_txt, region FROM staging.raw_gtd WHERE country IS NOT NULL;

-- 3. Geography & Group (Le tabelle con SERIAL)
INSERT INTO rd.geography (country_id, provstate, city, latitude, longitude)
SELECT DISTINCT 
    country, 
    COALESCE(provstate, ''), 
    COALESCE(city, ''), 
    COALESCE(latitude, 0), 
    COALESCE(longitude, 0)
FROM staging.raw_gtd 
WHERE country IS NOT NULL;

INSERT INTO rd.terrorist_group (gname, gsubname, claimed)
SELECT DISTINCT 
    gname, 
    COALESCE(gsubname, ''), 
    COALESCE(CAST(claimed AS INT)::BOOLEAN, false)
FROM staging.raw_gtd 
WHERE gname IS NOT NULL;

-- 4. Event Core Fact
INSERT INTO rd.event (
    eventid, iyear, imonth, iday, full_date, is_approximate_date, 
    success, suicide, nkill, nkillter, nwound, propvalue, 
    loc_id, group_id, attacktype_id, nkillter_reported
)
SELECT 
    s.eventid, s.iyear, s.imonth, s.iday, s.full_date, s.is_approximate_date, 
    CAST(s.success AS INT)::BOOLEAN, CAST(s.suicide AS INT)::BOOLEAN, s.nkill, s.nkillter, s.nwound, s.propvalue,
    g.loc_id, tg.group_id, s.attacktype1, s.nkillter_reported
FROM staging.raw_gtd s
-- Join pulito e 1:1, dato che le dimensioni ora sono "appiattite" correttamente
LEFT JOIN rd.geography g ON 
    s.country = g.country_id AND 
    COALESCE(s.provstate, '') = g.provstate AND 
    COALESCE(s.city, '') = g.city AND 
    COALESCE(s.latitude, 0) = g.latitude AND 
    COALESCE(s.longitude, 0) = g.longitude
LEFT JOIN rd.terrorist_group tg ON 
    s.gname = tg.gname AND 
    COALESCE(s.gsubname, '') = tg.gsubname AND 
    COALESCE(CAST(s.claimed AS INT)::BOOLEAN, false) = tg.claimed;

-- 5. Bridge Tables M:N
INSERT INTO rd.event_weapon (eventid, weaptype_id)
SELECT DISTINCT eventid, weaptype1 FROM staging.raw_gtd WHERE weaptype1 IS NOT NULL;

INSERT INTO rd.event_target (eventid, targtype_id)
SELECT DISTINCT eventid, targtype1 FROM staging.raw_gtd WHERE targtype1 IS NOT NULL;