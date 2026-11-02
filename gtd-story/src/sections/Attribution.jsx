import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, ArrowUpRight } from '../components/ui/Icons';
import { fmt } from '../lib/format';
import Reveal from '../components/ui/Reveal';
import SectionLabel from '../components/ui/SectionLabel';
import { weaponStyle } from '../lib/viz';
const groupNames = {
  'Islamic State of Iraq and the Levant (ISIL)': 'ISIS / ISIL',
  'Shining Path (SL)': 'Shining Path',
  "New People's Army (NPA)": 'New People’s Army',
  'Farabundo Marti National Liberation Front (FMLN)': 'FMLN',
  'Houthi extremists (Ansar Allah)': 'Houthi / Ansar Allah',
  'Irish Republican Army (IRA)': 'IRA',
  "Kurdistan Workers' Party (PKK)": 'PKK',
};
const weapons = {
  Explosives: 'Esplosivi',
  Firearms: 'Armi da fuoco',
  Unknown: 'Non note',
  Incendiary: 'Incendiarie',
  Melee: 'Armi bianche',
  Other: 'Altre',
  Chemical: 'Chimiche',
  'Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)': 'Veicoli',
  'Sabotage Equipment': 'Equipaggiamento di sabotaggio',
  Biological: 'Biologiche',
  'Fake Weapons': 'Armi finte',
  Radiological: 'Radiologiche',
};
export default function Attribution({ data }) {
  const [index, setIndex] = useState(0),
    [sort, setSort] = useState('events');
  const groups = [...data.groups].sort((a, b) => b[sort] - a[sort]),
    group = data.groups[index],
    top = groups[0][sort];
  return (
    <section id="gruppi" className="attribution-section section-space">
      <div className="wrap">
        <Reveal>
          <SectionLabel number="03">Gli autori e l’assenza di un nome</SectionLabel>
          <div className="attribution-intro">
            <h2>
              Quasi un evento su due.
              <br />
              <span>Senza un autore noto.</span>
            </h2>
            <div className="unknown-highlight">
              <strong>
                43,8<span>%</span>
              </strong>
              <p>
                degli eventi non è attribuito
                <br />a un gruppo conosciuto.
              </p>
            </div>
          </div>
          <div className="attribution-strip">
            <div className="unknown-share">
              <span>43,8% · Autore ignoto</span>
            </div>
            <div className="known-share">
              <span>56,2% · Autore noto</span>
            </div>
          </div>
          <p className="attribution-context">
            E dove un nome c’è, la responsabilità è frammentata:{' '}
            <strong>{fmt(data.totals.knownGroups)} gruppi distinti.</strong>
            <br />I primi dieci coprono il <strong>39,7%</strong> dei casi attribuiti.
          </p>
        </Reveal>
        <Reveal className="group-panel">
          <div className="panel-heading">
            <div>
              <h3>I dieci gruppi più frequenti</h3>
              <p>Seleziona un gruppo per scoprirne le armi utilizzate.</p>
            </div>
            <div className="segmented" role="group" aria-label="Ordina i dieci gruppi">
              <button aria-pressed={sort === 'events'} onClick={() => setSort('events')}>
                Per eventi
              </button>
              <button aria-pressed={sort === 'deaths'} onClick={() => setSort('deaths')}>
                Per decessi
              </button>
            </div>
          </div>
          <div className="group-layout">
            <div className="group-bars">
              {groups.map((g, i) => (
                <button
                  className={`group-row ${g.gname === group.gname ? 'selected' : ''}`}
                  key={g.gname}
                  onClick={() => setIndex(data.groups.findIndex((x) => x.gname === g.gname))}
                  aria-pressed={g.gname === group.gname}
                  title={g.gname}
                >
                  <span className="group-rank">{String(i + 1).padStart(2, '0')}</span>
                  <span className="group-row-content">
                    <span className="group-row-label">
                      <span>{groupNames[g.gname] || g.gname}</span>
                      <strong>{fmt(g[sort])}</strong>
                    </span>
                    <span className="group-bar-track">
                      <motion.i
                        initial={false}
                        animate={{ scaleX: g[sort] / top }}
                        transition={{ duration: 0.5, ease: [0.23, 1, 0.32, 1] }}
                      />
                    </span>
                  </span>
                  <ArrowUpRight className="group-arrow" size={15} />
                </button>
              ))}
            </div>
            <aside className="weapon-detail" aria-live="polite">
              <span className="eyebrow">DENTRO IL GRUPPO</span>
              <h3>{groupNames[group.gname] || group.gname}</h3>
              <div className="weapon-group-stats">
                <div>
                  <strong>{fmt(group.events)}</strong>
                  <span>eventi</span>
                </div>
                <div>
                  <strong>{fmt(group.lethality, 2)}</strong>
                  <span>decessi / evento</span>
                </div>
              </div>
              <div className="weapon-caption">ARMI PRIMARIE UTILIZZATE</div>
              <div className="weapon-composition" aria-hidden="true">
                {group.weapons.map((w, i) => (
                  <div
                    key={w.weapon_name}
                    style={{ flex: w.events, background: weaponStyle(w.weapon_name).color }}
                  />
                ))}
              </div>
              <div className="weapons-list">
                {group.weapons.map((w, i) => (
                  <div key={w.weapon_name}>
                    <span>
                      <i style={{ background: weaponStyle(w.weapon_name).color }} />
                      {weapons[w.weapon_name] || w.weapon_name}
                    </span>
                    <strong>
                      {(w.events / group.events) * 100 < 0.05
                        ? '<0,1'
                        : fmt((w.events / group.events) * 100, 1)}
                      %
                    </strong>
                  </div>
                ))}
              </div>
              <p className="detail-context">
                Un’arma primaria per evento.
                <br />
                Colori stabili per categoria d’arma in tutti i gruppi. Quote arrotondate.
              </p>
            </aside>
          </div>
          <div className="chart-footnote">
            <span>
              Il riordino per decessi confronta gli stessi dieci gruppi selezionati per numero di
              eventi.
            </span>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
