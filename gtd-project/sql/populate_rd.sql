/*
   FASE 2 - POPOLAMENTO DEL RECONCILED DATABASE
   staging.raw_gtd  ->  schema rd
 */


INSERT INTO rd.geography (country_id, provstate, city, lat_centroid, lon_centroid)
SELECT COALESCE(CAST(s.country AS INT), -1),
       COALESCE(NULLIF(TRIM(s.provstate), ''), 'Unknown'),
       COALESCE(NULLIF(TRIM(s.city), ''), 'Unknown'),
       ROUND(CAST(AVG(s.latitude)  AS NUMERIC), 6),
       ROUND(CAST(AVG(s.longitude) AS NUMERIC), 6)
FROM staging.raw_gtd s
GROUP BY COALESCE(CAST(s.country AS INT), -1),
         COALESCE(NULLIF(TRIM(s.provstate), ''), 'Unknown'),
         COALESCE(NULLIF(TRIM(s.city), ''), 'Unknown');


INSERT INTO rd.terrorist_group (gname, gsubname)
SELECT DISTINCT
       COALESCE(NULLIF(TRIM(s.gname), ''), 'Unknown'),
       COALESCE(NULLIF(TRIM(s.gsubname), ''), '')
FROM staging.raw_gtd s;


INSERT INTO rd.event (
    eventid, iyear, imonth, iday, full_date, is_approximate_date,
    loc_id, latitude, longitude, specificity, vicinity,
    group_id, claimed, guncertain1, nperps,
    attacktype_id, natlty_id,
    success, suicide, extended, multiple,
    nkill, nkillter, nwound, property, propextent, propvalue,
    crit1, crit2, crit3, doubtterr,
    nkillter_reported, is_nkill_imputed, is_nwound_imputed
)
SELECT
    CAST(s.eventid AS BIGINT),
    CAST(s.iyear AS SMALLINT),
    CAST(s.imonth AS SMALLINT),
    CAST(s.iday AS SMALLINT),
    s.full_date,
    COALESCE(s.is_approximate_date, FALSE),

    g.loc_id,
    ROUND(CAST(s.latitude  AS NUMERIC), 6),
    ROUND(CAST(s.longitude AS NUMERIC), 6),
    CASE WHEN CAST(s.specificity AS INT) BETWEEN 1 AND 5 THEN CAST(s.specificity AS SMALLINT) END,
    CASE WHEN CAST(s.vicinity AS INT) = 1 THEN TRUE WHEN CAST(s.vicinity AS INT) = 0 THEN FALSE END,

    tg.group_id,
    CASE WHEN CAST(s.claimed AS INT) = 1 THEN TRUE WHEN CAST(s.claimed AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.guncertain1 AS INT) = 1 THEN TRUE WHEN CAST(s.guncertain1 AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.nperps AS INT) >= 0 THEN CAST(s.nperps AS INT) END,

    COALESCE(NULLIF(NULLIF(CAST(s.attacktype1 AS INT), -9), -99), -1),
    COALESCE(NULLIF(NULLIF(CAST(s.natlty1 AS INT), -9), -99), -1),

    CASE WHEN CAST(s.success AS INT)  = 1 THEN TRUE WHEN CAST(s.success AS INT)  = 0 THEN FALSE END,
    CASE WHEN CAST(s.suicide AS INT)  = 1 THEN TRUE WHEN CAST(s.suicide AS INT)  = 0 THEN FALSE END,
    CASE WHEN CAST(s.extended AS INT) = 1 THEN TRUE WHEN CAST(s.extended AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.multiple AS INT) = 1 THEN TRUE WHEN CAST(s.multiple AS INT) = 0 THEN FALSE END,

    CASE WHEN CAST(s.nkill    AS INT) >= 0 THEN CAST(s.nkill    AS INT) END,
    CASE WHEN CAST(s.nkillter AS INT) >= 0 THEN CAST(s.nkillter AS INT) END,
    CASE WHEN CAST(s.nwound   AS INT) >= 0 THEN CAST(s.nwound   AS INT) END,
    CASE WHEN CAST(s.property AS INT) = 1 THEN TRUE WHEN CAST(s.property AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.propextent AS INT) BETWEEN 1 AND 4 THEN CAST(s.propextent AS SMALLINT) END,
    CASE WHEN CAST(s.propvalue AS NUMERIC) >= 0 THEN CAST(s.propvalue AS NUMERIC) END,

    CASE WHEN CAST(s.crit1 AS INT) = 1 THEN TRUE WHEN CAST(s.crit1 AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.crit2 AS INT) = 1 THEN TRUE WHEN CAST(s.crit2 AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.crit3 AS INT) = 1 THEN TRUE WHEN CAST(s.crit3 AS INT) = 0 THEN FALSE END,
    CASE WHEN CAST(s.doubtterr AS INT) = 1 THEN TRUE WHEN CAST(s.doubtterr AS INT) = 0 THEN FALSE END,

    CASE WHEN CAST(s.nkillter_reported AS INT) = 1 THEN TRUE ELSE FALSE END,
    CASE WHEN CAST(s.is_nkill_imputed  AS INT) = 1 THEN TRUE ELSE FALSE END,
    CASE WHEN CAST(s.is_nwound_imputed AS INT) = 1 THEN TRUE ELSE FALSE END

FROM staging.raw_gtd s
JOIN rd.geography g
  ON g.country_id = COALESCE(CAST(s.country AS INT), -1)
 AND g.provstate  = COALESCE(NULLIF(TRIM(s.provstate), ''), 'Unknown')
 AND g.city       = COALESCE(NULLIF(TRIM(s.city), ''), 'Unknown')
JOIN rd.terrorist_group tg
  ON tg.gname    = COALESCE(NULLIF(TRIM(s.gname), ''), 'Unknown')
 AND tg.gsubname = COALESCE(NULLIF(TRIM(s.gsubname), ''), '');


INSERT INTO rd.event_weapon (eventid, weapsubtype_id, weap_order)
SELECT u.eventid,
       COALESCE(u.sid, 9000 + u.wid) AS weapsubtype_id,
       MIN(u.slot)
FROM (
    SELECT CAST(s.eventid AS BIGINT) AS eventid,
           CAST(s.weaptype1 AS INT) AS wid,
           NULLIF(NULLIF(CAST(s.weapsubtype1 AS INT), -9), -99) AS sid,
           1 AS slot
    FROM staging.raw_gtd s WHERE s.weaptype1 IS NOT NULL
    UNION ALL
    SELECT CAST(s.eventid AS BIGINT), CAST(s.weaptype2 AS INT),
           NULLIF(NULLIF(CAST(s.weapsubtype2 AS INT), -9), -99), 2
    FROM staging.raw_gtd s WHERE s.weaptype2 IS NOT NULL
    UNION ALL
    SELECT CAST(s.eventid AS BIGINT), CAST(s.weaptype3 AS INT),
           NULLIF(NULLIF(CAST(s.weapsubtype3 AS INT), -9), -99), 3
    FROM staging.raw_gtd s WHERE s.weaptype3 IS NOT NULL
    UNION ALL
    SELECT CAST(s.eventid AS BIGINT), CAST(s.weaptype4 AS INT),
           NULLIF(NULLIF(CAST(s.weapsubtype4 AS INT), -9), -99), 4
    FROM staging.raw_gtd s WHERE s.weaptype4 IS NOT NULL
) u
WHERE u.wid NOT IN (-1, -9, -99)
  AND EXISTS (SELECT 1 FROM rd.event e WHERE e.eventid = u.eventid)
GROUP BY u.eventid, COALESCE(u.sid, 9000 + u.wid);

INSERT INTO rd.event_target (eventid, targsubtype_id, targ_order)
SELECT u.eventid,
       COALESCE(u.sid, 9000 + u.tid) AS targsubtype_id,
       MIN(u.slot)
FROM (
    SELECT CAST(s.eventid AS BIGINT) AS eventid,
           CAST(s.targtype1 AS INT) AS tid,
           NULLIF(NULLIF(CAST(s.targsubtype1 AS INT), -9), -99) AS sid,
           1 AS slot
    FROM staging.raw_gtd s WHERE s.targtype1 IS NOT NULL
    UNION ALL
    SELECT CAST(s.eventid AS BIGINT), CAST(s.targtype2 AS INT),
           NULLIF(NULLIF(CAST(s.targsubtype2 AS INT), -9), -99), 2
    FROM staging.raw_gtd s WHERE s.targtype2 IS NOT NULL
    UNION ALL
    SELECT CAST(s.eventid AS BIGINT), CAST(s.targtype3 AS INT),
           NULLIF(NULLIF(CAST(s.targsubtype3 AS INT), -9), -99), 3
    FROM staging.raw_gtd s WHERE s.targtype3 IS NOT NULL
) u
WHERE u.tid NOT IN (-1, -9, -99)
  AND EXISTS (SELECT 1 FROM rd.event e WHERE e.eventid = u.eventid)
GROUP BY u.eventid, COALESCE(u.sid, 9000 + u.tid);

CREATE OR REPLACE VIEW rd.dq_hierarchy_conflicts AS
WITH osservato AS (
    SELECT 'arma'::TEXT AS dimensione, CAST(s.weapsubtype1 AS INT) AS figlio, CAST(s.weaptype1 AS INT) AS padre FROM staging.raw_gtd s WHERE s.weapsubtype1 IS NOT NULL AND s.weaptype1 IS NOT NULL
    UNION ALL SELECT 'arma', CAST(s.weapsubtype2 AS INT), CAST(s.weaptype2 AS INT) FROM staging.raw_gtd s WHERE s.weapsubtype2 IS NOT NULL AND s.weaptype2 IS NOT NULL
    UNION ALL SELECT 'arma', CAST(s.weapsubtype3 AS INT), CAST(s.weaptype3 AS INT) FROM staging.raw_gtd s WHERE s.weapsubtype3 IS NOT NULL AND s.weaptype3 IS NOT NULL
    UNION ALL SELECT 'arma', CAST(s.weapsubtype4 AS INT), CAST(s.weaptype4 AS INT) FROM staging.raw_gtd s WHERE s.weapsubtype4 IS NOT NULL AND s.weaptype4 IS NOT NULL
    UNION ALL SELECT 'bersaglio', CAST(s.targsubtype1 AS INT), CAST(s.targtype1 AS INT) FROM staging.raw_gtd s WHERE s.targsubtype1 IS NOT NULL AND s.targtype1 IS NOT NULL
    UNION ALL SELECT 'bersaglio', CAST(s.targsubtype2 AS INT), CAST(s.targtype2 AS INT) FROM staging.raw_gtd s WHERE s.targsubtype2 IS NOT NULL AND s.targtype2 IS NOT NULL
    UNION ALL SELECT 'bersaglio', CAST(s.targsubtype3 AS INT), CAST(s.targtype3 AS INT) FROM staging.raw_gtd s WHERE s.targsubtype3 IS NOT NULL AND s.targtype3 IS NOT NULL
    UNION ALL SELECT 'geografia', CAST(s.country AS INT), CAST(s.region AS INT) FROM staging.raw_gtd s WHERE s.country IS NOT NULL AND s.region IS NOT NULL
),
conteggio AS (
    SELECT dimensione, figlio, padre, COUNT(*) AS righe_sorgente
    FROM osservato
    WHERE figlio NOT IN (-1, -9, -99) AND padre NOT IN (-1, -9, -99)
    GROUP BY dimensione, figlio, padre
),
assegnato AS (
    SELECT 'arma'::TEXT AS dimensione, weapsubtype_id AS figlio, weaptype_id AS padre, weapon_subtype_name AS nome
    FROM rd.weapon_subtype WHERE weapsubtype_id BETWEEN 0 AND 8999
    UNION ALL
    SELECT 'bersaglio', targsubtype_id, targtype_id, target_subtype_name
    FROM rd.target_subtype WHERE targsubtype_id BETWEEN 0 AND 8999
    UNION ALL
    SELECT 'geografia', country_id, region_id, country_name
    FROM rd.country WHERE country_id >= 0
),
ambigui AS (
    SELECT dimensione, figlio
    FROM conteggio
    GROUP BY dimensione, figlio
    HAVING COUNT(*) > 1
)
SELECT c.dimensione,
       c.figlio,
       a.nome                       AS figlio_nome,
       a.padre                      AS padre_assegnato,
       c.padre                      AS padre_osservato,
       c.righe_sorgente,
       (c.padre = a.padre)          AS assegnato,
       (c.righe_sorgente = MAX(c.righe_sorgente) OVER (PARTITION BY c.dimensione, c.figlio)) AS maggioritario
FROM conteggio c
JOIN ambigui   m ON m.dimensione = c.dimensione AND m.figlio = c.figlio
JOIN assegnato a ON a.dimensione = c.dimensione AND a.figlio = c.figlio
ORDER BY c.dimensione, c.figlio, c.righe_sorgente DESC;


DO $$
DECLARE
    n_violazioni INT;
    dettaglio    TEXT;
BEGIN
    SELECT COUNT(*), STRING_AGG(dimensione || ' #' || figlio || ' (' || COALESCE(figlio_nome, '?') || ')', ', ')
      INTO n_violazioni, dettaglio
      FROM rd.dq_hierarchy_conflicts
     WHERE assegnato AND NOT maggioritario;

    IF n_violazioni > 0 THEN
        RAISE EXCEPTION 'Gerarchia incoerente: % membri hanno ricevuto un padre MINORITARIO nella sorgente -> %',
                        n_violazioni, dettaglio;
    END IF;

    RAISE NOTICE 'Gerarchie verificate: ogni membro ha il padre maggioritario. Conflitti documentati in rd.dq_hierarchy_conflicts: %',
                 (SELECT COUNT(DISTINCT (dimensione, figlio)) FROM rd.dq_hierarchy_conflicts);
END $$;
