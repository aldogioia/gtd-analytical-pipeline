TRUNCATE TABLE
    rd.event_target, rd.event_weapon, rd.event,
    rd.target_subtype, rd.target_type,
    rd.weapon_subtype, rd.weapon_type,
    rd.attack_type, rd.terrorist_group,
    rd.geography, rd.country, rd.region
RESTART IDENTITY CASCADE;


INSERT INTO rd.region (region_id, region_name, macro_area)
SELECT h.region_id, h.region_name, h.macro_area
FROM staging.hier_region h;

INSERT INTO rd.country (country_id, country_name, region_id)
SELECT h.country_id, h.country_name, h.region_id
FROM staging.hier_country h;


INSERT INTO rd.attack_type (attacktype_id, attack_name, attack_macro)
SELECT h.attacktype_id, h.attack_name, h.attack_macro
FROM staging.hier_attack_type h;


INSERT INTO rd.weapon_type (weaptype_id, weapon_name, weapon_macro, weapon_group)
SELECT h.weaptype_id, h.weapon_name, h.weapon_macro, h.weapon_group
FROM staging.hier_weapon_type h;

INSERT INTO rd.weapon_subtype (weapsubtype_id, weapon_subtype_name, weaptype_id)
SELECT h.weapsubtype_id, h.weapon_subtype_name, h.weaptype_id
FROM staging.hier_weapon_subtype h;


INSERT INTO rd.target_type (targtype_id, target_name, target_macro)
SELECT h.targtype_id, h.target_name, h.target_macro
FROM staging.hier_target_type h;

INSERT INTO rd.target_subtype (targsubtype_id, target_subtype_name, targtype_id)
SELECT h.targsubtype_id, h.target_subtype_name, h.targtype_id
FROM staging.hier_target_subtype h;

DO $$
DECLARE
    n INT;
BEGIN
    SELECT COUNT(*) INTO n
    FROM rd.weapon_subtype ws
    JOIN rd.weapon_type wt ON wt.weaptype_id = ws.weaptype_id
    WHERE ws.weapsubtype_id IN (7, 8, 11, 16, 17)
      AND wt.weapon_name <> 'Explosives';
    IF n > 0 THEN
        RAISE EXCEPTION 'Gerarchia arma incoerente: % sottotipi esplosivi non stanno sotto Explosives', n;
    END IF;
END $$;


DO $$
DECLARE
    n INT;
BEGIN
    SELECT COUNT(*) INTO n
    FROM rd.target_subtype ts
    JOIN rd.target_type tt ON tt.targtype_id = ts.targtype_id
    WHERE ts.targsubtype_id IN (68, 113)
      AND tt.target_name <> 'Private Citizens & Property';
    IF n > 0 THEN
        RAISE EXCEPTION 'Gerarchia bersaglio incoerente: % sottotipi civili non stanno sotto Private Citizens & Property', n;
    END IF;
END $$;


DO $$
DECLARE
    n INT;
BEGIN
    SELECT COUNT(*) INTO n
    FROM rd.weapon_type wt
    WHERE wt.weaptype_id <> -1
      AND NOT EXISTS (SELECT 1 FROM rd.weapon_subtype ws
                      WHERE ws.weaptype_id = wt.weaptype_id
                        AND ws.weapon_subtype_name = 'Not Specified');
    IF n > 0 THEN
        RAISE EXCEPTION 'Mancano % segnaposto "Not Specified" nella gerarchia arma', n;
    END IF;
END $$;