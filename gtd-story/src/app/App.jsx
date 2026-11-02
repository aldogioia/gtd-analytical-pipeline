import { useState, useEffect } from 'react';
import { motion, useScroll, useSpring, useReducedMotion } from 'framer-motion';
import {
  ArrowUpRight,
  ArrowDown,
  Globe2,
  Menu,
  X,
  Database,
  Info,
  GitHub,
} from '../components/ui/Icons';
import Globe from '../components/visualizations/Globe';
import Timeline from '../sections/Timeline';
import Tactics from '../sections/Tactics';
import Attribution from '../sections/Attribution';
import Method from '../sections/Method';
import Reveal from '../components/ui/Reveal';
import Count from '../components/ui/Count';
import SectionLabel from '../components/ui/SectionLabel';

const chapters = [
  ['geografia', 'Il mondo'],
  ['tattiche', 'Le tattiche'],
  ['gruppi', 'Gli autori'],
  ['metodo', 'Il metodo'],
  ['sintesi', 'Conclusioni'],
];
export default function App() {
  const [data, setData] = useState(null),
    [locations, setLocations] = useState(null),
    [mapLocations, setMapLocations] = useState(null),
    [error, setError] = useState(false),
    [menu, setMenu] = useState(false),
    [active, setActive] = useState('');
  const reduce = useReducedMotion();
  const { scrollYProgress } = useScroll();
  const progress = useSpring(scrollYProgress, { stiffness: 100, damping: 30, restDelta: 0.001 });
  useEffect(() => {
    let alive = true;
    Promise.all([
      fetch('/data/story.json').then((r) => {
        if (!r.ok) throw Error();
        return r.json();
      }),
      fetch('/data/locations.json').then((r) => {
        if (!r.ok) throw Error();
        return r.json();
      }),
      fetch('/data/map-locations.json').then((r) => {
        if (!r.ok) throw Error();
        return r.json();
      }),
    ])
      .then(([d, l, m]) => {
        if (alive) {
          setData(d);
          setLocations(l);
          setMapLocations(m);
        }
      })
      .catch(() => {
        if (alive) setError(true);
      });
    return () => {
      alive = false;
    };
  }, []);
  useEffect(() => {
    if (!data) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: '-20% 0px -55% 0px', threshold: 0 },
    );
    document.querySelectorAll('main section[id]').forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [data]);
  return (
    <>
      <a className="skip-link" href="#contenuto">
        Vai al contenuto
      </a>
      <header className="site-header">
        <div className="nav-wrap">
          <a className="brand" href="#inizio" aria-label="GTD, torna all’inizio">
            <Globe2 size={23} strokeWidth={1.3} />
            <span>
              GTD
              <span className="brand-divider" />
              Data stories
            </span>
          </a>
          <nav aria-label="Capitoli del racconto" className={menu ? 'open' : ''}>
            {chapters.map(([id, title]) => (
              <a
                key={id}
                href={'#' + id}
                aria-current={active === id ? 'location' : undefined}
                onClick={() => setMenu(false)}
              >
                {title}
              </a>
            ))}
          </nav>
          <div className="header-actions">
            <button
              className="menu-button icon-button"
              onClick={() => setMenu(!menu)}
              aria-expanded={menu}
              aria-label={menu ? 'Chiudi menu' : 'Apri menu'}
            >
              {menu ? <X /> : <Menu />}
            </button>
          </div>
        </div>
        <motion.div
          className="page-progress"
          style={{ scaleX: reduce ? scrollYProgress : progress }}
        />
      </header>
      <main id="contenuto">
        <section id="inizio" className="hero">
          <div className="hero-globe">
            <Globe locations={locations} hero />
            <div className="globe-caption">
              <span className="live-dot" />
              209.706 eventi. Un unico pianeta.
            </div>
            <div className="hero-coordinate">
              <span>1970 — 2020</span>
              <span>GLOBAL TERRORISM DATABASE</span>
            </div>
          </div>
          <div className="hero-content">
            <Reveal>
              <div className="eyebrow hero-eyebrow">
                <span className="tiny-line" /> DATA WAREHOUSE & VISUALIZATION
              </div>
              <h1>
                Il terrorismo
                <br />
                globale <span>nei dati.</span>
              </h1>
              <p className="hero-subtitle">Dal dato grezzo alla decisione analitica.</p>
              <p className="hero-description">
                Cinquant’anni di eventi. Una prospettiva diversa.
                <br />
                Esplora come cambiano scala, gravità e attribuzione
                <br className="desktop-break" /> del terrorismo nel mondo, dal 1970 al 2020.
              </p>
              <div className="hero-ctas">
                <a className="button primary" href="#geografia">
                  Esplora la storia <ArrowDown size={17} />
                </a>
                <a className="text-button" href="#metodo">
                  Dentro il progetto <ArrowUpRight size={15} />
                </a>
              </div>
            </Reveal>
          </div>
          <div className="hero-bottom">
            <div className="kpis">
              {[
                [209706, 0, '', 'Attentati registrati'],
                [523944, 0, '', 'Decessi complessivi'],
                [10.68, 2, '%', 'Attacchi transnazionali'],
              ].map(([v, d, s, l]) => (
                <div className="kpi" key={l}>
                  <div className="kpi-number">
                    <Count value={v} decimals={d} suffix={s} />
                  </div>
                  <div className="kpi-label">{l}</div>
                </div>
              ))}
            </div>
            <div className="scroll-hint">
              <span>SCORRI PER SCOPRIRE</span>
              <ArrowDown size={16} />
            </div>
          </div>
        </section>
        {error ? (
          <div className="load-error">
            <h2>I dati non sono stati caricati.</h2>
            <p>Controlla la connessione e ricarica la pagina.</p>
            <button className="button primary" onClick={() => window.location.reload()}>
              Riprova
            </button>
          </div>
        ) : !data ? (
          <div className="loading-state" role="status">
            Caricamento delle visualizzazioni…
          </div>
        ) : (
          <>
            <Timeline data={data} locations={mapLocations} />
            <Tactics data={data} />
            <Attribution data={data} />
            <Method data={data} />
            <section id="sintesi" className="conclusion wrap">
              <Reveal>
                <SectionLabel number="05">Le conclusioni</SectionLabel>
                <h2>
                  Tre idee.
                  <br />
                  <span>Una lettura più consapevole.</span>
                </h2>
              </Reveal>
              <div className="conclusion-grid">
                {[
                  {
                    n: '01',
                    tag: 'TEMPO E GEOGRAFIA',
                    title: 'Il picco è concentrato.',
                    text: 'Il 2014 è il massimo storico. L’Iraq pesa per quasi un terzo dei decessi di quell’anno.',
                    icon: Globe2,
                  },
                  {
                    n: '02',
                    tag: 'FREQUENZA E GRAVITÀ',
                    title: 'Più frequente non significa più letale.',
                    text: 'Gli assalti armati causano in media 4,15 decessi per evento. Le esplosioni, più frequenti, 1,82.',
                    icon: Database,
                  },
                  {
                    n: '03',
                    tag: 'QUALITÀ E ATTRIBUZIONE',
                    title: 'L’attribuzione resta il limite.',
                    text: 'Il 43,8% degli eventi non ha un autore noto. I gruppi conosciuti formano una lunga coda.',
                    icon: Info,
                  },
                ].map((c, i) => (
                  <Reveal className="conclusion-card" key={c.n} delay={i * 0.06}>
                    <div className="card-top">
                      <c.icon size={23} strokeWidth={1.3} />
                      <span>{c.n}</span>
                    </div>
                    <span className="eyebrow">{c.tag}</span>
                    <h3>{c.title}</h3>
                    <p>{c.text}</p>
                  </Reveal>
                ))}
              </div>
              <Reveal className="closing">
                <p>
                  Il valore non è avere più dati.
                  <br />
                  <span>È poter verificare ogni conclusione.</span>
                </p>
                <a
                  className="repository-link"
                  href="https://github.com/aldogioia/gtd-analytical-pipeline"
                  target="_blank"
                  rel="noreferrer"
                >
                  <GitHub size={18} /> Codice e pipeline su GitHub <ArrowUpRight size={16} />
                </a>
              </Reveal>
            </section>
          </>
        )}
      </main>
      <footer className="site-footer wrap">
        <div>
          <a className="brand" href="#inizio">
            <Globe2 size={21} strokeWidth={1.3} />
            <span>
              GTD <span className="footer-brand">Data stories</span>
            </span>
          </a>
          <p>
            Un progetto di Aldo Gioia
            <br />
            Data Warehouse & Visualization · A.A. 2025–2026
          </p>
        </div>
        <div className="footer-notes">
          <p>
            Fonte: Global Terrorism Database · START
            <br />
            Dati riconciliati, osservati e stimati · 1970–2020
          </p>
          <div className="footer-source-links">
            <a href="/data/story.json" download="gtd-aggregazioni.json">
              Dati <ArrowDown size={12} />
            </a>
          </div>
          <p className="footer-measure-note">
            Decessi osservati e stimati. Quota transnazionale sui casi classificabili.
          </p>
        </div>
        <a className="back-top" href="#inizio" aria-label="Torna all’inizio">
          <ArrowDown size={19} />
        </a>
      </footer>
    </>
  );
}
