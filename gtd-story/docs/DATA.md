# Dati, misure e riproducibilità

## Provenienza

Il sito usa gli export dimensionali di `../gtd-project/dataset/dwh_export/`. I documenti originali sono in `../Presentation & Report/`; la cartella dei documenti e le relative copie PDF sono escluse dalla pubblicazione.

Le visualizzazioni contengono aggregazioni reali, non dati simulati. Il sito racconta il modello originale; non addestra né esegue modelli nel browser.

## Misure principali

- 209.706 attentati.
- 523.944 decessi: 479.348 osservati e 44.596 stimati.
- 12.527 eventi con conteggio dei morti imputato.
- Quota transnazionale del 10,68%, calcolata sui 207.692 eventi classificabili.
- 1993 senza rilevazioni disponibili: un vuoto informativo, non zero eventi.

Armi e bersagli usano il solo arco primario delle bridge table (`is_primary = true`), per conservare eventi e decessi durante le aggregazioni.

## Riconciliazione temporale

La dimensione tempo esportata non comprende il 31 dicembre 2020. Per i 18 eventi interessati, che contano 45 decessi, lo script recupera l’anno dal parquet originale tramite `eventid`. La timeline include così tutti gli eventi. Il warehouse originale non viene modificato.

## File geografici

- `public/data/locations.json`: coordinate valide raggruppate per anno e arrotondate a 0,01°; righe `[latitudine, longitudine, eventi, decessi]`.
- `public/data/map-locations.json`: celle di 2° × 2°, collocate sulla media delle coordinate reali e con somme esatte di eventi e decessi.
- `src/data/land-points.json`: geometria statica del globo, precalcolata con D3 per evitare calcoli geografici durante il caricamento della pagina.

Le coordinate mancanti non vengono collocate artificialmente sulla mappa. Il numero di eventi geolocalizzati è distinto dal totale.

## Modello

La pipeline originale usa LightGBM in due passaggi: riconoscere il regime senza vittime e stimare i conteggi positivi. I risultati rispettano i vincoli di dominio e vengono convertiti in interi con il metodo dei resti maggiori.

Sul campione di verifica il modello dei morti ha un bias sul totale di −1,49%; quello dei feriti di −22,99%. Il secondo non viene adottato e i valori mancanti restano tali.

Il report completo resta nel materiale locale `Presentation & Report/`, escluso da Git e dalla build pubblica.

## Ricostruzione e controlli

`build_data.py` richiede pandas e pyarrow e usa la cartella `gtd-project/` adiacente alla repo. L’output è risolto rispetto alla repo stessa, senza dipendere dal nome `gtd-story`.

`npm run verify:data` controlla totali, serie annuale, gap del 1993, sottoinsiemi suicidi, armi per gruppo, coordinate e conservazione di eventi e decessi in ogni anno delle celle geografiche.

I JSON generati sono versionati perché costituiscono gli input del sito. Build, dipendenze, cache e appunti locali sono esclusi da Git.
