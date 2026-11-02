import { severityStops } from '../../lib/viz';
export default function VizLegend({ size = false, unit = 'eventi', map = false }) {
  return (
    <div className="viz-legend">
      {size && (
        <div className="size-legend">
          <svg viewBox="0 0 90 30" aria-hidden="true">
            <circle cx="14" cy="20" r="3" />
            <circle cx="40" cy="17" r="6" />
            <circle cx="73" cy="12" r="11" />
          </svg>
          <span>Area ∝ numero di {unit}</span>
        </div>
      )}
      <div className="severity-legend">
        <div>
          <span>Letalità media</span>
          <span>decessi / evento</span>
        </div>
        <div
          className="severity-ramp"
          style={{
            background: `linear-gradient(90deg,${severityStops.map(([n, c]) => `${c} ${n * 10}%`).join(',')})`,
          }}
        />
        <div className="severity-ticks">
          <span>0</span>
          <span>2</span>
          <span>5</span>
          <span>10+</span>
        </div>
      </div>
      {map && (
        <p className="legend-explanation">
          Una bolla per cella di 2° × 2°. Posizione media degli eventi, area proporzionale al
          numero. Scala fissa per tutti gli anni.
        </p>
      )}
    </div>
  );
}
