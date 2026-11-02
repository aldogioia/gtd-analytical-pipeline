# Global Terrorism Database — Analytical Pipeline & Data Story

Un progetto unico, dal dato grezzo alla narrazione interattiva del terrorismo globale, 1970–2020.

- **`gtd-project/`** — pipeline Python, riconciliazione PostgreSQL, star schema, modelli e workbook Tableau.
- **`gtd-story/`** — scrollstory React con mappa, confronti interattivi e metodo spiegato in modo accessibile.
- **`scripts/`** — pubblicazione della build su GitHub Pages.
- **`docs/`** — istruzioni per il dominio e il rilascio.

## Scrollstory

Richiede Node.js 22.12+ e npm.

```sh
npm ci
npm run dev
```

Anteprima: <http://127.0.0.1:5173/>.

```sh
npm run verify:data
npm run build
npm run deploy:check
npm run deploy
```

`deploy` costruisce il sito e pubblica **solo `gtd-story/dist/`** sul ramo `gh-pages`. La cronologia di `main` e i file di lavoro non vengono modificati. Il comando usa un checkout temporaneo e un normale push, senza force-push. È disponibile anche da `gtd-story/` con `npm run deploy`.

Sito previsto: <https://gtd.aldogioia.com>. Configurazione DNS e Pages: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Pipeline

Installazione e comandi: [gtd-project/README.md](gtd-project/README.md).

Il pacchetto Python mantiene separati estrazione, qualità, gerarchie, imputazione, caricamento e riconciliazione. L’export e l’addestramento hanno punti di ingresso dedicati. Nessuna credenziale di database è incorporata nel codice.

Le aggregazioni pubbliche del sito sono già incluse. Per rigenerarle, dopo avere esportato il warehouse:

```sh
gtd-project/.venv/bin/python gtd-story/scripts/build_data.py
npm run verify:data
```

## Contenuti esclusi

`Presentation & Report/`, le copie dei relativi PDF, ambienti virtuali, dipendenze, cache, build, riferimenti locali e backup non entrano in Git né nel sito. Il `.gitignore` è condiviso dalla radice. La cache Parquet e i bundle dei modelli già presenti nel progetto restano disponibili nella cartella della pipeline; gli export CSV del warehouse sono output locali rigenerabili.

Dettagli sulle misure e sulla riconciliazione temporale: [gtd-story/docs/DATA.md](gtd-story/docs/DATA.md).
