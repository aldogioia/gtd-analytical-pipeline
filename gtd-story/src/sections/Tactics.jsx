import { useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { ArrowUpRight, ArrowRight, Info } from '../components/ui/Icons';
import { fmt } from '../lib/format';
import Reveal from '../components/ui/Reveal';
import SectionLabel from '../components/ui/SectionLabel';
import VizLegend from '../components/visualizations/VizLegend';
import { severityColor } from '../lib/viz';
const labels = {
  'Bombing/Explosion': 'Esplosioni',
  'Armed Assault': 'Assalti armati',
  Assassination: 'Assassinii',
  'Hostage Taking (Kidnapping)': 'Rapimenti',
  'Facility/Infrastructure Attack': 'Attacchi a infrastrutture',
  Unknown: 'Non classificati',
  'Unarmed Assault': 'Assalti non armati',
  'Hostage Taking (Barricade Incident)': 'Presa di ostaggi',
  Hijacking: 'Dirottamenti',
};
const targets = {
  'State and Security': 'Stato e sicurezza',
  'Civilian and Society': 'Civili e società',
  Economic: 'Attività economiche',
  'Infrastructure and Transport': 'Infrastrutture e trasporti',
  'Other or Unknown': 'Altro / non noto',
  'Armed Non State Actors': 'Attori armati non statali',
};
function Scatter({ items, selected, onSelect, logScale = false, volumeMax }) {
  const reduce = useReducedMotion(),
    W = 760,
    H = 405,
    L = 54,
    R = 24,
    T = 26,
    B = 54;
  const maxX = Math.ceil(Math.max(...items.map((x) => x.events)) / 1000 / 2) * 2000,
    maxY = Math.ceil(Math.max(...items.map((x) => x.lethality)) / 2) * 2;
  const x = (v) => L + (v / maxX) * (W - L - R),
    y = (v) => H - B - (logScale ? Math.log1p(v) / Math.log1p(maxY) : v / maxY) * (H - T - B);
  const tickValues = logScale
    ? [0, 1, 10, 100, maxY]
    : Array.from({ length: 5 }, (_, i) => (i * maxY) / 4);
  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      className="scatter-chart"
      role="img"
      aria-label="Frequenza e letalità per modalità di attacco. Asse orizzontale: numero di eventi. Asse verticale: decessi medi per evento. Usa anche i pulsanti sotto il grafico."
    >
      <text className="axis-caption" x={L} y={12}>
        {logScale
          ? 'DECESSI MEDI PER EVENTO · SCALA LOGARITMICA (LOG1P)'
          : 'DECESSI MEDI PER EVENTO'}
      </text>
      {tickValues.map((v) => {
        return (
          <g key={v}>
            <line x1={L} x2={W - R} y1={y(v)} y2={y(v)} className="chart-grid" />
            <text x={L - 13} y={y(v) + 4} textAnchor="end" className="axis-text">
              {fmt(v, Number.isInteger(v) ? 0 : 1)}
            </text>
          </g>
        );
      })}
      {Array.from({ length: 5 }, (_, i) => {
        const v = (i * maxX) / 4;
        return (
          <text key={i} x={x(v)} y={H - B + 23} textAnchor="middle" className="axis-text">
            {v === 0 ? '0' : fmt(v / 1000, Number.isInteger(v / 1000) ? 0 : 1) + 'k'}
          </text>
        );
      })}
      <text x={W - R} y={H - 5} textAnchor="end" className="axis-caption">
        NUMERO DI ATTENTATI →
      </text>
      {items.map((d, i) => {
        let dx = 14,
          dy = -13,
          anchor = 'start';
        if (d.attack_name === 'Bombing/Explosion') {
          dx = -15;
          dy = -30;
          anchor = 'end';
        }
        if (d.attack_name === 'Unknown') {
          dx = 14;
          dy = -18;
        }
        if (d.attack_name === 'Hijacking') {
          dx = 14;
          dy = -13;
        }
        if (d.attack_name === 'Unarmed Assault') {
          dy = -14;
        }
        if (d.attack_name === 'Hostage Taking (Barricade Incident)') {
          dy = 19;
        }
        const main = ['Bombing/Explosion', 'Armed Assault'].includes(d.attack_name);
        const active = selected === d.attack_name;
        const radius = Math.sqrt(d.events / volumeMax) * 22;
        return (
          <motion.g
            key={d.attack_name}
            initial={false}
            animate={{ x: x(d.events), y: y(d.lethality) }}
            transition={{ duration: reduce ? 0 : 0.55, ease: [0.23, 1, 0.32, 1] }}
            className={`scatter-point ${active ? 'is-selected' : ''}`}
            onClick={() => onSelect(d.attack_name)}
            style={{ cursor: 'pointer' }}
          >
            <title>
              {labels[d.attack_name]}: {fmt(d.events)} eventi, {fmt(d.lethality, 2)} decessi per
              evento
            </title>
            {active && <circle r={radius + 7} className="point-halo" />}
            <circle r={Math.max(12, radius)} fill="transparent" />
            <circle
              r={radius}
              style={{
                fill: severityColor(d.lethality),
                stroke: active ? '#f0f0f0' : '#0b0d10',
                strokeWidth: active ? 1.5 : 0.7,
              }}
              className="point-data"
              strokeDasharray={d.attack_name === 'Unknown' ? '2 2' : undefined}
            />
            <text
              x={dx}
              y={dy}
              textAnchor={anchor}
              className={`${main || active ? 'point-label' : 'point-label secondary-label' + (logScale ? ' log-secondary' : '')}`}
            >
              {labels[d.attack_name]}
            </text>
          </motion.g>
        );
      })}
    </svg>
  );
}
export default function Tactics({ data }) {
  const [mode, setMode] = useState('all'),
    [selected, setSelected] = useState('Armed Assault');
  const rows = data.attacks[mode],
    chosen = rows.find((x) => x.attack_name === selected) || rows[0],
    suicide = data.suicide.find((x) => x.is_suicide === 1),
    regular = data.suicide.find((x) => x.is_suicide === 0),
    targetRows = data.targets[mode],
    maxTarget = Math.max(...targetRows.map((t) => t.events));
  const suicideYears = data.years.filter((x) => x.events !== null),
    maxSuicide = Math.max(...suicideYears.map((x) => x.suicide));
  return (
    <section id="tattiche" className="tactics-section section-space wrap">
      <Reveal>
        <SectionLabel number="02">Frequenza e gravità</SectionLabel>
        <div className="section-heading">
          <h2>
            Più frequente.
            <br />
            <span>Non sempre più letale.</span>
          </h2>
          <p>
            Le esplosioni dominano per numero.
            <br />
            Gli assalti armati per impatto medio.
            <br />
            Due misure, due letture diverse.
          </p>
        </div>
      </Reveal>
      <Reveal className="chart-panel">
        <div className="panel-heading">
          <div>
            <h3>La matrice delle tattiche</h3>
            <p>1970–2020 · Seleziona una modalità per esplorarla</p>
          </div>
          <div className="segmented" role="group" aria-label="Filtra per attacchi suicidi">
            <button aria-pressed={mode === 'all'} onClick={() => setMode('all')}>
              Tutti gli eventi
            </button>
            <button aria-pressed={mode === 'suicide'} onClick={() => setMode('suicide')}>
              Solo suicidi
            </button>
          </div>
        </div>
        <div className="scatter-layout">
          <div className="scatter-container">
            <Scatter
              items={rows}
              selected={chosen.attack_name}
              onSelect={setSelected}
              logScale={mode === 'suicide'}
              volumeMax={Math.max(...data.attacks.all.map((x) => x.events))}
            />
          </div>
          <aside className="tactic-detail" aria-live="polite">
            <span className="eyebrow">MODALITÀ SELEZIONATA</span>
            <h4>{labels[chosen.attack_name]}</h4>
            <div className="detail-number">
              {fmt(chosen.lethality, 2)}
              <small>decessi per evento</small>
            </div>
            <div className="detail-pair">
              <span>Attentati</span>
              <strong>{fmt(chosen.events)}</strong>
            </div>
            <div className="detail-pair">
              <span>Decessi</span>
              <strong>{fmt(chosen.deaths)}</strong>
            </div>
            <span className="detail-context">
              {mode === 'suicide'
                ? 'Solo eventi con indicatore suicida. Le medie su pochi casi sono sensibili agli eventi estremi.'
                : 'Valori osservati e stimati dal warehouse.'}
            </span>
          </aside>
        </div>
        <VizLegend size />
        <div className="chart-selector" role="group" aria-label="Modalità di attacco">
          {rows.map((d) => (
            <button
              key={d.attack_name}
              aria-pressed={chosen.attack_name === d.attack_name}
              onClick={() => setSelected(d.attack_name)}
            >
              {labels[d.attack_name]}
            </button>
          ))}
        </div>
        <div className="chart-footnote">
          <Info size={13} />
          <span>
            {mode === 'suicide'
              ? 'Letalità = decessi / eventi. Scala verticale logaritmica (log1p). Area e colore conservano la stessa scala del totale.'
              : 'Letalità = decessi / eventi. La categoria “non classificati” resta visibile per rendere esplicita l’incertezza.'}
          </span>
        </div>
      </Reveal>
      <div className="tactics-bottom">
        <Reveal className="suicide-story">
          <span className="eyebrow">UNA MINORANZA AD ALTO IMPATTO</span>
          <h3>
            Gli attacchi suicidi.
            <br />
            <span>Una gravità diversa.</span>
          </h3>
          <p>
            Il {fmt((suicide.events / data.totals.events) * 100, 1)}% degli eventi è suicida, ma la
            letalità media è {fmt(suicide.lethality / regular.lethality, 1)} volte quella degli
            altri attacchi.
          </p>
          <div className="suicide-kpis">
            <div>
              <strong>{fmt(suicide.lethality, 2)}</strong>
              <span>decessi / evento suicida</span>
            </div>
            <div>
              <strong>{fmt(regular.lethality, 2)}</strong>
              <span>negli altri eventi</span>
            </div>
          </div>
          <div
            className="suicide-spark"
            role="img"
            aria-label="Numero di attacchi suicidi per anno, dal 1970 al 2020"
          >
            {data.years.map((y) => (
              <div
                key={y.year}
                className={y.year === 1993 ? 'missing' : ''}
                title={`${y.year}: ${y.events === null ? 'dati mancanti' : fmt(y.suicide) + ' eventi suicidi'}`}
              >
                <i style={{ height: `${Math.max(1, (y.suicide / maxSuicide) * 100)}%` }} />
              </div>
            ))}
          </div>
          <div className="spark-axis">
            <span>1970</span>
            <span>ATTACCHI SUICIDI NEL TEMPO</span>
            <span>2020</span>
          </div>
        </Reveal>
        <Reveal className="target-chart" delay={0.06}>
          <div className="target-chart-head">
            <h3>Chi viene colpito?</h3>
            <span>{mode === 'all' ? 'TUTTI GLI EVENTI' : 'SOLO SUICIDI'}</span>
          </div>
          <p>Lunghezza: eventi · Colore: decessi per evento.</p>
          {targetRows.map((t) => (
            <div className="target-row" key={t.target_macro}>
              <div>
                <span>{targets[t.target_macro] || t.target_macro}</span>
                <strong>
                  {fmt(t.events)} <small>{fmt(t.lethality, 2)} / evento</small>
                </strong>
              </div>
              <div className="bar-track">
                <motion.div
                  style={{ backgroundColor: severityColor(t.lethality) }}
                  initial={false}
                  animate={{ scaleX: t.events / maxTarget }}
                  transition={{ duration: 0.5, ease: [0.23, 1, 0.32, 1] }}
                />
              </div>
            </div>
          ))}
          <span className="chart-caption">Il filtro della matrice aggiorna anche i bersagli.</span>
        </Reveal>
      </div>
    </section>
  );
}
