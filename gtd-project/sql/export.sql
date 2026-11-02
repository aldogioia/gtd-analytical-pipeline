/*
   FASE 3 - CONSEGNA DELLO SCHEMA A STELLA ALLO STRUMENTO DI BI

   Ogni relazione e' estratta come entita' autonoma con la propria grana:
   il fatto, le otto dimensioni e le due bridge. Nessuna tabella unica
   denormalizzata: lo star join viene ricostruito dal front-end sulle
   chiavi surrogate.

   Fan-out: filtrando le bridge su is_primary = TRUE somme e conteggi sono
   esatti; senza filtro si ottiene l'analisi d'impatto, dove i totali non
   si conservano e gli eventi si contano con COUNT(DISTINCT eventid).

   Ogni blocco e' preceduto da '--@table: <nome>', che gtd_pipeline.cli.export usa
   per instradare il risultato. L'ORDER BY rende l'estrazione riproducibile.
*/


-- @table: fact_event
SELECT event_sk, eventid,
       date_sk, geo_sk, attack_country_sk, target_nat_sk,
       group_sk, attack_sk, quality_sk,
       latitude, longitude,
       nkill, nkillter, nkill_victims, nwound, casualties,
       nperps, propvalue,
       is_success, is_suicide, is_extended, is_multiple, is_transnational,
       n_weapon_types, n_target_types
FROM dwh.fact_event
ORDER BY event_sk;


--@table: dim_time
SELECT date_sk, full_date, iyear, decade, quarter,
       imonth, month_name, iday, day_of_week, day_name, is_weekend
FROM dwh.dim_time
ORDER BY date_sk;


--@table: dim_geography
SELECT geo_sk, loc_nk, city, provstate, country_name, region_name,
       lat_centroid, lon_centroid
FROM dwh.dim_geography
ORDER BY geo_sk;


--@table: dim_country
SELECT country_sk, country_nk, country_name, region_name
FROM dwh.dim_country
ORDER BY country_sk;


--@table: dim_group
SELECT group_sk, group_nk, gname, gsubname, is_unknown_perpetrator
FROM dwh.dim_group
ORDER BY group_sk;


--@table: dim_attack_type
SELECT attack_sk, attack_nk, attack_name, attack_macro
FROM dwh.dim_attack_type
ORDER BY attack_sk;


--@table: dim_weapon
SELECT weapon_sk, weapon_nk, weapon_subtype, weapon_name, weapon_macro
FROM dwh.dim_weapon
ORDER BY weapon_sk;


--@table: dim_target
SELECT target_sk, target_nk, target_subtype, target_name, target_macro
FROM dwh.dim_target
ORDER BY target_sk;


--@table: dim_quality
SELECT quality_sk, date_accuracy, nkill_source, nwound_source,
       perp_fatalities_source, claim_of_responsibility,
       perpetrator_attribution, doubt_terrorism, inclusion_criteria
FROM dwh.dim_quality
ORDER BY quality_sk;


--@table: bridge_event_weapon
SELECT event_sk, weapon_sk, is_primary
FROM dwh.bridge_event_weapon
ORDER BY event_sk, weapon_sk;


--@table: bridge_event_target
SELECT event_sk, target_sk, is_primary
FROM dwh.bridge_event_target
ORDER BY event_sk, target_sk;
