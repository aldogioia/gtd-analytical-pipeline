/*
   PROPAGAZIONE DEI NUOVI LIVELLI ALLE DIMENSIONI DELLO STAR SCHEMA
*/

UPDATE dwh.dim_country d
SET macro_area = r.macro_area
FROM rd.country c
JOIN rd.region r ON r.region_id = c.region_id
WHERE d.country_nk = c.country_id;

UPDATE dwh.dim_geography g
SET macro_area = r.macro_area
FROM rd.region r
WHERE r.region_name = g.region_name;

UPDATE dwh.dim_weapon d
SET weapon_group = wt.weapon_group
FROM rd.weapon_subtype ws
JOIN rd.weapon_type wt ON wt.weaptype_id = ws.weaptype_id
WHERE d.weapon_nk = ws.weapsubtype_id;


DO $$
DECLARE
    n INT;
BEGIN
    SELECT COUNT(*) INTO n
    FROM dwh.dim_weapon d
    JOIN rd.weapon_subtype ws ON ws.weapsubtype_id = d.weapon_nk
    JOIN rd.weapon_type wt ON wt.weaptype_id = ws.weaptype_id
    WHERE d.weapon_group <> wt.weapon_group;
    IF n > 0 THEN
        RAISE EXCEPTION 'weapon_group non propagato su % membri di dim_weapon', n;
    END IF;

    SELECT COUNT(*) INTO n
    FROM dwh.dim_country d
    JOIN rd.country c ON c.country_id = d.country_nk
    JOIN rd.region r ON r.region_id = c.region_id
    WHERE d.macro_area <> r.macro_area;
    IF n > 0 THEN
        RAISE EXCEPTION 'macro_area non propagata su % membri di dim_country', n;
    END IF;

    SELECT COUNT(DISTINCT macro_area) INTO n
    FROM dwh.dim_country WHERE macro_area <> 'Unknown';
    IF n <> 6 THEN
        RAISE EXCEPTION 'dim_country espone % macro-aree valorizzate, attese 6', n;
    END IF;
END $$;
