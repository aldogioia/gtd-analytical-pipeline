# GTD — Il terrorismo globale nei dati

Web app di scrollytelling per il progetto di Aldo Gioia, Data Warehouse & Visualization, A.A. 2025–2026.

## Avvio locale

Dalla radice della monorepo, con Node.js 22.12+:

```sh
npm ci
npm run dev
```

Aprire [http://127.0.0.1:5173/](http://127.0.0.1:5173/). La pubblicazione su GitHub Pages è esplicita: `npm run deploy`. Vedi [la guida di rilascio](../docs/DEPLOYMENT.md).

## Struttura

```text
src/
  app/                     pagina e navigazione
  sections/                capitoli del racconto
  components/
    ui/                    icone, contatori e transizioni condivise
    visualizations/        globo, mappa e legende
  lib/                     formattazione e scale visive
  data/                    geometrie precalcolate del globo
  styles/                  base, visualizzazioni e metodo
public/
  data/                    aggregazioni usate dal sito
scripts/                   preparazione e verifica dei dati
docs/                      provenienza, misure e riproducibilità
```

I capitoli non dipendono dalla pagina principale: componenti, formattazione e scale sono condivisi tramite moduli dedicati. Il metodo contiene quattro passaggi brevi e tre sottosezioni che spiegano come il modello valuta l’assenza di vittime, stima il conteggio e controlla il risultato.

## Comandi

```sh
npm run dev           # anteprima con aggiornamento automatico
npm run build         # build di produzione in dist/
npm run preview       # anteprima della build
npm run verify:data   # controlli di conservazione delle misure
npm run format        # formattazione del codice e della documentazione
npm run format:check  # verifica della formattazione
```

La formattazione esclude dati e geometrie generati, documenti PDF, dipendenze e materiali locali.

## Dati e documenti

Le aggregazioni necessarie alla visualizzazione sono versionate: il sito funziona senza eseguire la pipeline originale. Per ricostruire i dati servono gli export nella cartella vicina `gtd-project/`.

```sh
../gtd-project/.venv/bin/python scripts/build_data.py
npm run build:globe
npm run verify:data
```

Dettagli sulle misure, sul 1993 e sulla riconciliazione temporale: [docs/DATA.md](docs/DATA.md).

## Design e interazione

React, Vite, Three.js, D3, Framer Motion e Hugeicons (Stroke Rounded). Layout responsive, focus visibile e supporto a movimento ridotto. La mappa conserva scale di area e colore confrontabili fra gli anni. Il globo viene renderizzato su richiesta.

Riferimenti di design: [Apple Design](https://github.com/dickwu/apple-design-skill) e [Emil Kowalski](https://github.com/emilkowalski/skills). Le copie di lavoro e gli appunti estratti dai PDF sono conservati in `.local/references/`, esclusi da Git. I metadati della precedente pubblicazione sono archiviati in `.local/legacy/`.

Il `.gitignore` esclude dipendenze, build, cache, ambienti locali, log e materiali di lavoro. Mantiene versionati codice, lockfile, aggregazioni, geometrie e documenti necessari al sito.
