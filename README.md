# Il terrorismo globale nei dati

**Dal dato grezzo alla comprensione di cinquant’anni di terrorismo.**

Un progetto di Data Warehousing e Visualizzazione che esplora il Global Terrorism Database nel periodo **1970–2020**, unendo analisi dei dati, machine learning e narrazione interattiva.

[**Esplora la scrollstory → gtd.aldogioia.com**](https://gtd.aldogioia.com)

## Le domande

Come cambiano le geografie del terrorismo? Gli attacchi più frequenti sono anche i più letali? Quanto sappiamo dei gruppi responsabili?

La scrollstory accompagna queste domande con una mappa temporale e visualizzazioni interattive di tattiche, bersagli e autori. Il metodo entra nel racconto per mostrare da dove arrivano i numeri e quali limiti conservano.

## I dati

| Misura                                |                             Valore |
| ------------------------------------- | ---------------------------------: |
| Attentati registrati                  |                            209.706 |
| Decessi osservati                     |                            479.348 |
| Decessi stimati per i valori mancanti |                             44.596 |
| Attacchi transnazionali               | 10,68% degli eventi classificabili |

I conteggi osservati e quelli stimati restano distinguibili. Il 1993, privo di rilevazioni disponibili, viene rappresentato come un vuoto informativo.

## Cosa emerge

- **Il picco è concentrato.** Il 2014 e l’Iraq segnano una concentrazione decisiva degli eventi.
- **Frequenza e gravità non coincidono.** Le modalità di attacco più diffuse non sono necessariamente le più letali.
- **L’attribuzione resta un limite.** Nel 43,8% degli eventi non è noto un gruppo responsabile.

## Dietro il racconto

La base analitica organizza i dati in PostgreSQL, riconcilia luoghi e categorie e permette di confrontare gli eventi senza duplicarli. Un modello LightGBM in due stadi stima i conteggi mancanti dei morti, rispettando le informazioni già note.

La stessa scelta non viene estesa ai feriti: l’errore sui totali nel campione di verifica sarebbe troppo elevato. Rendere visibili questi limiti è parte del progetto.

Il repository raccoglie la pipeline analitica, il modello dati, le analisi Tableau e la web app di scrollytelling.

---

Progetto universitario di **Aldo Gioia** · Data Warehouse & Visualization · A.A. 2025–2026.
