# GTD analytical pipeline

Pipeline riproducibile per Global Terrorism Database: qualità dei dati, PostgreSQL 3NF, star schema e imputazione dei morti mancanti con LightGBM.

## Struttura

```text
gtd_pipeline/
  cli/          export CSV e addestramento
  db/           connessioni, caricamento e runner SQL
  etl/          estrazione, pulizia, gerarchie e riconciliazione
  models/       modelli e strategie di imputazione
sql/            schemi, popolamento ed export
tableau/        workbook di analisi
docs/           codebook e checklist
tests/          verifiche senza connessione al database
tools/          utilità di analisi e manutenzione del workbook
```

## Installazione

Python 3.10+ e PostgreSQL. Dalla cartella `gtd-project/`:

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
cp .env.example .env
```

Impostare le proprie credenziali in `.env`, escluso da Git, e caricarle nella shell:

```sh
set -a
source .env
set +a
```

La sorgente Excel si imposta con `GTD_SOURCE`; se esiste `dataset/gtd_raw.parquet`, viene usata la cache. Le altre opzioni sono definite in `gtd_pipeline/config.py`.

## Comandi

```sh
.venv/bin/python -m gtd_pipeline --help
.venv/bin/python -m gtd_pipeline
.venv/bin/python -m gtd_pipeline.cli.train --help
.venv/bin/python -m gtd_pipeline.cli.train
.venv/bin/python -m gtd_pipeline.cli.export
```

Dopo l’installazione editable sono disponibili anche `gtd-pipeline`, `gtd-train` e `gtd-export`.

La pipeline completa ricostruisce gli schemi `staging`, `rd` e `dwh` nel database configurato. `--bootstrap` si ferma dopo lo staging senza imputazione; `--sql-only` ripete la parte SQL. Questi comandi modificano il database configurato: le verifiche di sviluppo qui sotto non lo fanno.

## Verifiche

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Il workbook è in `tableau/GTD.twb`. Esportare prima i CSV con il comando dedicato e, se necessario, aggiornare le connessioni Tableau alla cartella `dataset/dwh_export/` e al proprio estratto Hyper.
