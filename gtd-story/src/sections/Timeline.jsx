import { useState, useRef, useEffect } from 'react';
import { useScroll, useMotionValueEvent, useReducedMotion } from 'framer-motion';
import { Play, Pause, RotateCcw, ArrowDown } from '../components/ui/Icons';
import WorldMap from '../components/visualizations/WorldMap';
import VizLegend from '../components/visualizations/VizLegend';
import { fmt } from '../lib/format';
import SectionLabel from '../components/ui/SectionLabel';
const story = (y) =>
  y === 1993
    ? {
        title: 'Il vuoto non è uno zero.',
        text: 'Le rilevazioni del 1993 non sono disponibili. La serie mantiene esplicita questa interruzione.',
      }
    : y < 1990
      ? {
          title: 'Una distribuzione che attraversa i continenti.',
          text: 'La mappa mostra l’insieme degli eventi dell’anno: il totale globale va sempre letto nel contesto geografico.',
        }
      : y < 2005
        ? {
            title: 'La frequenza non descrive tutta la gravità.',
            text: 'Confronta bolle di dimensione simile: un colore più caldo indica più decessi medi per evento.',
          }
        : y < 2014
          ? {
              title: 'La crescita si concentra in alcune aree.',
              text: 'Dalla metà degli anni Duemila il numero di eventi aumenta. Osserva come cambia la distribuzione nello spazio.',
            }
          : y === 2014
            ? {
                title: '2014 · Il massimo della serie.',
                text: '16.960 attentati, 49.713 decessi. L’Iraq conta 3.934 eventi e il 30,1% dei decessi dell’anno.',
              }
            : y < 2017
              ? {
                  title: 'Dopo il picco, livelli ancora elevati.',
                  text: 'La scala resta fissa: il confronto con il 2014 conserva il significato di area e colore.',
                }
              : {
                  title: 'Meno eventi non significa assenza di impatto.',
                  text: 'La frequenza diminuisce rispetto al 2014. La letalità media e la geografia aggiungono il contesto.',
                };
export default function Timeline({ data, locations }) {
  const section = useRef(),
    intro = useRef(),
    [year, setYear] = useState(1970),
    [manual, setManual] = useState(false),
    [playing, setPlaying] = useState(false),
    follow = useRef(true),
    reduce = useReducedMotion();
  const { scrollYProgress } = useScroll({ target: section, offset: ['start start', 'end end'] });
  const yearAt = (v) => 1970 + Math.round(Math.max(0, Math.min(1, (v - 0.035) / 0.965)) * 50);
  useMotionValueEvent(scrollYProgress, 'change', (v) => {
    const t = Math.max(0, Math.min(1, v / 0.035));
    if (intro.current) {
      intro.current.style.opacity = String(1 - t);
      intro.current.style.transform = reduce ? 'none' : `translateY(${-28 * t}px)`;
    }
    if (follow.current) setYear(yearAt(v));
  });
  const select = (y) => {
    follow.current = false;
    setManual(true);
    setPlaying(false);
    setYear(y);
  };
  const resume = () => {
    follow.current = true;
    setManual(false);
    setPlaying(false);
    setYear(yearAt(scrollYProgress.get()));
  };
  useEffect(() => {
    if (!playing) return;
    const timer = setInterval(
      () =>
        setYear((y) => {
          if (y >= 2020) {
            setPlaying(false);
            return 2020;
          }
          return y + 1;
        }),
      800,
    );
    return () => clearInterval(timer);
  }, [playing]);
  const item = data.years.find((x) => x.year === year),
    n = story(year),
    max = Math.max(...data.years.map((y) => y.events || 0)),
    rows = locations?.[year] || [],
    geoTotal = rows.reduce((s, r) => s + r[2], 0);
  return (
    <section id="geografia" ref={section} className="map-chapter">
      <div className="map-sticky wrap">
        <div ref={intro} className="map-chapter-intro">
          <SectionLabel number="01">Il mondo, nel tempo</SectionLabel>
          <h2>
            Cinquant’anni.
            <br />
            <span>Geografie che cambiano.</span>
          </h2>
          <span className="intro-scroll">
            <ArrowDown size={14} /> Scorri per leggere la mappa
          </span>
        </div>
        <div className="map-dashboard">
          <div className="map-dashboard-head">
            <div className="map-year">
              <span className="eyebrow">ANNO</span>
              <strong>{year}</strong>
            </div>
            <div className="map-year-stats" aria-live={manual ? 'polite' : 'off'}>
              <div>
                <strong>{item.events === null ? '—' : fmt(item.events)}</strong>
                <span>attentati</span>
              </div>
              <div>
                <strong>{item.deaths === null ? '—' : fmt(item.deaths)}</strong>
                <span>decessi</span>
              </div>
              <div>
                <strong>{item.events === null ? '—' : fmt(item.deaths / item.events, 2)}</strong>
                <span>decessi / evento</span>
              </div>
            </div>
          </div>
          <div className="map-narrative">
            <strong>{n.title}</strong>
            <p>{n.text}</p>
          </div>
          <WorldMap rows={rows} year={year} />
          <div className="map-support">
            <VizLegend size map />
            <div className="map-country-summary">
              <span className="eyebrow">PIÙ EVENTI NELL’ANNO</span>
              <div>
                {item.countries.slice(0, 3).map((c, i) => (
                  <span key={c.country_name}>
                    <b>
                      {i + 1}. {c.country_name}
                    </b>
                    <span>{fmt(c.events)}</span>
                  </span>
                ))}
              </div>
              <small>
                {year === 1993
                  ? 'Nessuna rilevazione disponibile'
                  : `${fmt(geoTotal)} eventi con coordinate valide su ${fmt(item.events)}.`}
              </small>
            </div>
          </div>
          <div className="map-time-controls">
            <div className="timeline-control-header">
              <span>ATTENTATI PER ANNO · 1970–2020</span>
              <div>
                {manual ? (
                  <button className="text-button resume-scroll" onClick={resume}>
                    <RotateCcw size={12} /> Segui lo scroll
                  </button>
                ) : (
                  <span className="gap-label">Lo scroll avanza nel tempo</span>
                )}
                <button
                  className="icon-button play-button"
                  aria-label={
                    playing ? 'Ferma la sequenza temporale' : 'Riproduci la sequenza temporale'
                  }
                  aria-pressed={playing}
                  onClick={() => {
                    follow.current = false;
                    setManual(true);
                    if (!playing && year === 2020) setYear(1970);
                    setPlaying(!playing);
                  }}
                >
                  {playing ? <Pause size={15} /> : <Play size={15} />}
                </button>
              </div>
            </div>
            <div className="year-bars" role="group" aria-label="Seleziona un anno">
              {data.years.map((y) => (
                <button
                  key={y.year}
                  aria-label={`${y.year}: ${y.events === null ? 'dati mancanti' : fmt(y.events) + ' attentati'}`}
                  aria-pressed={year === y.year}
                  title={`${y.year} · ${y.events === null ? 'Dati mancanti' : fmt(y.events) + ' eventi'}`}
                  onClick={() => select(y.year)}
                  className={`year-bar ${y.year === year ? 'selected' : ''} ${y.events === null ? 'missing' : ''}`}
                >
                  <span
                    style={{
                      height:
                        y.events === null ? '100%' : `${Math.max(3, (y.events / max) * 100)}%`,
                    }}
                  />
                </button>
              ))}
            </div>
            <label className="sr-only" htmlFor="year-slider">
              Anno da visualizzare
            </label>
            <input
              id="year-slider"
              className="year-range"
              type="range"
              min="1970"
              max="2020"
              value={year}
              onChange={(e) => select(+e.target.value)}
              aria-valuetext={`${year}${year === 1993 ? ', dati mancanti' : ''}`}
            />
            <div className="year-axis">
              {[1970, 1980, 1990, 2000, 2010, 2020].map((y) => (
                <span key={y}>{y}</span>
              ))}
            </div>
            <p className="map-data-note">
              1993: rilevazioni mancanti. Valori osservati e stimati; le coordinate assenti non sono
              collocate sulla mappa.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
