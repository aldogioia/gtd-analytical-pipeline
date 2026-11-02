import ModelArchitecture from './ModelArchitecture';
import { useState, useRef } from 'react';
import {
  motion,
  AnimatePresence,
  useScroll,
  useMotionValueEvent,
  useReducedMotion,
} from 'framer-motion';
import { Calendar, Globe2, Users, RotateCcw } from '../components/ui/Icons';
import { fmt } from '../lib/format';
import SectionLabel from '../components/ui/SectionLabel';
import { easeOut } from '../lib/viz';

const chapters = [
  {
    name: 'Ordine',
    title: (
      <>
        Un evento.
        <br />
        <span>Un solo conteggio.</span>
      </>
    ),
    text: 'Organizziamo anni, luoghi e autori. Ogni attentato viene contato una sola volta.',
  },
  {
    name: 'Trasparenza',
    title: (
      <>
        Colmare i vuoti.
        <br />
        <span>Senza nasconderli.</span>
      </>
    ),
    text: 'Nel 6% degli eventi manca il numero dei morti. Lo stimiamo, distinguendolo sempre dai valori osservati.',
  },
  {
    name: 'Verifica',
    title: (
      <>
        Una stima serve.
        <br />
        <span>Se regge la prova.</span>
      </>
    ),
    text: 'La stima dei morti si discosta dal totale reale solo dell’1,49%.',
  },
  {
    name: 'Limiti',
    title: (
      <>
        A volte,
        <br />
        <span>è meglio fermarsi.</span>
      </>
    ),
    text: 'Per i feriti, la stima perderebbe quasi una persona su quattro. Il dato resta mancante.',
  },
];

function EventStructure({ events }) {
  return (
    <div
      className="method-event-visual"
      role="img"
      aria-label={`${fmt(events)} eventi, confrontabili per tempo, luogo e autore. Ogni evento viene contato una sola volta.`}
    >
      <span className="method-viz-label">IL PATRIMONIO DATI</span>
      <strong className="method-event-total">{fmt(events)}</strong>
      <span className="method-event-unit">eventi, senza duplicazioni</span>
      <svg
        className="method-connections"
        viewBox="0 0 540 75"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <path d="M270 0V26M90 75V45Q90 26 109 26H431Q450 26 450 45V75M270 26V75" />
      </svg>
      <div className="method-lenses">
        <span>
          <Calendar size={22} />
          Quando
        </span>
        <span>
          <Globe2 size={22} />
          Dove
        </span>
        <span>
          <Users size={22} />
          Chi
        </span>
      </div>
    </div>
  );
}
function MissingValues({ data }) {
  const estimated = data.totals.imputedEvents,
    observed = data.totals.events - estimated,
    share = estimated / data.totals.events;
  return (
    <div
      className="method-missing-visual"
      role="img"
      aria-label={`${fmt(observed)} eventi con conteggio dei morti osservato; ${fmt(estimated)} con conteggio stimato, pari al ${fmt(share * 100, 2)} per cento.`}
    >
      <span className="method-viz-label">DA DOVE ARRIVA IL NUMERO DEI MORTI</span>
      <div className="method-share-labels">
        <div>
          <strong>{fmt(observed)}</strong>
          <span>
            <i />
            Osservati
          </span>
        </div>
        <div>
          <strong>{fmt(estimated)}</strong>
          <span>
            <i />
            Stimati
          </span>
        </div>
      </div>
      <div className="method-share-bar" aria-hidden="true">
        <span style={{ flex: observed }} />
        <span style={{ flex: estimated }} />
      </div>
      <div className="method-share-percentages">
        <span>{fmt((1 - share) * 100, 1)}%</span>
        <span>{fmt(share * 100, 1)}%</span>
      </div>
      <p>Le stime rimangono riconoscibili in ogni analisi.</p>
    </div>
  );
}
function ModelComparison({ focus }) {
  const width = 560,
    left = 80,
    right = 95,
    x = (v) => left + ((v + 30) / 45) * (width - left - right),
    rows = [
      { name: 'Morti', value: -1.49, y: 100, color: '#9dbbd3', active: focus === 'deaths' },
      { name: 'Feriti', value: -22.99, y: 196, color: '#e49a82', active: focus === 'wounds' },
    ];
  return (
    <div className="method-model-visual">
      <span className="method-viz-label">DIFFERENZA DAL TOTALE REALE</span>
      <svg
        viewBox="0 0 560 270"
        role="img"
        aria-label="Scarto sul totale: morti meno 1,49 per cento, entro la tolleranza di più o meno 15 per cento. Feriti meno 22,99 per cento, fuori dalla tolleranza."
      >
        <rect
          x={x(-15)}
          width={x(15) - x(-15)}
          y="42"
          height="192"
          fill="#a8c5df"
          fillOpacity=".045"
        />
        <line x1={x(-15)} x2={x(-15)} y1="42" y2="234" stroke="#6e829b" strokeDasharray="3 5" />
        <line x1={x(0)} x2={x(0)} y1="42" y2="234" stroke="#7d8b9c" strokeOpacity=".55" />
        <text x={(x(-15) + x(15)) / 2} y="25" textAnchor="middle" className="model-tolerance-label">
          MARGINE ACCETTATO ±15%
        </text>
        {rows.map((r) => (
          <g key={r.name} opacity={r.active ? 1 : 0.8} className="method-model-row">
            <text x="0" y={r.y + 5} className="method-model-label">
              {r.name}
            </text>
            <line
              x1={left}
              x2={width - right}
              y1={r.y}
              y2={r.y}
              stroke="#536174"
              strokeOpacity=".4"
            />
            <line x1={x(r.value)} x2={x(0)} y1={r.y} y2={r.y} stroke={r.color} strokeWidth="2" />
            {r.active && (
              <circle cx={x(r.value)} cy={r.y} r="14" fill={r.color} fillOpacity=".09" />
            )}
            <circle cx={x(r.value)} cy={r.y} r="5" fill={r.color} />
            <text
              x={width}
              textAnchor="end"
              y={r.y + 5}
              fill={r.color}
              className="method-model-value"
            >
              {fmt(r.value, 2).replace('-', '−')}%
            </text>
          </g>
        ))}
        {[-30, -15, 0, 15].map((v) => (
          <text x={x(v)} y="260" textAnchor="middle" className="method-model-tick" key={v}>
            {v > 0 ? '+' : ''}
            {v}%
          </text>
        ))}
      </svg>
      <p>{focus === 'deaths' ? 'Morti: stima accettata.' : 'Feriti: stima non adottata.'}</p>
    </div>
  );
}
export default function Method({ data }) {
  const section = useRef(),
    follow = useRef(true),
    reduce = useReducedMotion();
  const [step, setStep] = useState(0),
    [manual, setManual] = useState(false),
    [instant, setInstant] = useState(false);
  const { scrollYProgress } = useScroll({ target: section, offset: ['start start', 'end end'] });
  const at = (v) => Math.min(chapters.length - 1, Math.max(0, Math.floor(v * chapters.length)));
  useMotionValueEvent(scrollYProgress, 'change', (v) => {
    if (follow.current) {
      setStep(at(v));
      setInstant(false);
    }
  });
  const select = (i, e) => {
    follow.current = false;
    setManual(true);
    setInstant(e.detail === 0);
    setStep(i);
  };
  const chapter = chapters[step],
    visualKey = step < 2 ? step : 'comparison';
  return (
    <>
      <section id="metodo" ref={section} className="method-story">
        <div className="method-sticky wrap">
          <div className="method-topline">
            <SectionLabel number="04">Il metodo, in poche parole</SectionLabel>
            <span>DAL DATO ALLA FIDUCIA</span>
          </div>
          <div className="method-layout">
            <div className="method-copy" aria-live={manual ? 'polite' : 'off'}>
              <span className="method-step-number">0{step + 1} / 04</span>
              <h2>{chapter.title}</h2>
              <p>{chapter.text}</p>
            </div>
            <div className="method-visual">
              <AnimatePresence mode="wait" initial={false}>
                <motion.div
                  key={visualKey}
                  className="method-visual-content"
                  initial={{
                    opacity: 0,
                    transform: reduce || instant ? 'none' : 'translateY(10px)',
                  }}
                  animate={{ opacity: 1, transform: 'translateY(0px)' }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: reduce || instant ? 0 : 0.2, ease: easeOut }}
                >
                  {step === 0 ? (
                    <EventStructure events={data.totals.events} />
                  ) : step === 1 ? (
                    <MissingValues data={data} />
                  ) : (
                    <ModelComparison focus={step === 2 ? 'deaths' : 'wounds'} />
                  )}
                </motion.div>
              </AnimatePresence>
            </div>
          </div>
          <div className="method-bottomline">
            <nav className="method-navigation" aria-label="Passi del metodo">
              {chapters.map((c, i) => (
                <button key={c.name} aria-pressed={step === i} onClick={(e) => select(i, e)}>
                  <span>0{i + 1}</span>
                  {c.name}
                </button>
              ))}
            </nav>
            <div className="method-scroll-control">
              {manual ? (
                <button
                  className="text-button"
                  onClick={() => {
                    follow.current = true;
                    setManual(false);
                    setStep(at(scrollYProgress.get()));
                  }}
                >
                  <RotateCcw size={13} /> Segui lo scroll
                </button>
              ) : (
                <span>Scorri per continuare</span>
              )}
            </div>
          </div>
        </div>
      </section>
      <ModelArchitecture />
    </>
  );
}
