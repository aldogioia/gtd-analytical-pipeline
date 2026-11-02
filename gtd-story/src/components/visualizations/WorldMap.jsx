import { useEffect, useRef, useState } from 'react';
import { geoNaturalEarth1, geoPath } from 'd3-geo';
import { feature } from 'topojson-client';
import topology from 'world-atlas/countries-110m.json';
import { severityColor } from '../../lib/viz';
import { fmt } from '../../lib/format';
const countries = feature(topology, topology.objects.countries);
export default function WorldMap({ rows = [], year }) {
  const host = useRef(),
    canvas = useRef(),
    hitPoints = useRef([]),
    [hover, setHover] = useState(null);
  useEffect(() => setHover(null), [year]);
  useEffect(() => {
    const el = canvas.current,
      box = host.current;
    const draw = () => {
      const width = box.clientWidth,
        height = box.clientHeight,
        dpr = Math.min(devicePixelRatio, 2);
      if (!width || !height) return;
      el.width = width * dpr;
      el.height = height * dpr;
      const ctx = el.getContext('2d');
      ctx.scale(dpr, dpr);
      const projection = geoNaturalEarth1().fitExtent(
          [
            [8, 8],
            [width - 8, height - 8],
          ],
          { type: 'Sphere' },
        ),
        path = geoPath(projection, ctx);
      ctx.clearRect(0, 0, width, height);
      ctx.beginPath();
      path(countries);
      ctx.fillStyle = '#1c2632';
      ctx.fill();
      ctx.strokeStyle = '#3c4b5c';
      ctx.lineWidth = 0.55;
      ctx.stroke();
      hitPoints.current = [];
      // Fixed coefficient: equal event counts always occupy equal area at a given viewport.
      const coefficient = (width / 1000) * 0.65;
      [...rows]
        .sort((a, b) => b[2] - a[2])
        .forEach(([lat, lng, n, deaths]) => {
          const [x, y] = projection([lng, lat]),
            r = Math.sqrt(n) * coefficient,
            color = severityColor(deaths / n);
          ctx.beginPath();
          ctx.arc(x, y, r, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.globalAlpha = 0.77;
          ctx.fill();
          ctx.globalAlpha = 1;
          ctx.strokeStyle = '#0b0d1080';
          ctx.lineWidth = 0.5;
          ctx.stroke();
          hitPoints.current.push({ x, y, r, n, deaths, lat, lng });
        });
    };
    const observer = new ResizeObserver(draw);
    observer.observe(box);
    draw();
    return () => observer.disconnect();
  }, [rows]);
  const inspect = (e) => {
    const rect = canvas.current.getBoundingClientRect(),
      x = e.clientX - rect.left,
      y = e.clientY - rect.top;
    let found = null,
      min = Infinity;
    for (const p of hitPoints.current) {
      const d = Math.hypot(x - p.x, y - p.y);
      if (d < Math.max(p.r, 8) && d < min) {
        found = p;
        min = d;
      }
    }
    setHover(found);
  };
  return (
    <div className="world-map" ref={host}>
      <canvas
        ref={canvas}
        onPointerMove={(e) => {
          if (e.pointerType === 'mouse') inspect(e);
        }}
        onClick={inspect}
        onPointerLeave={() => setHover(null)}
        role="img"
        aria-label={`Mappa mondiale ${year}. ${fmt(rows.reduce((s, r) => s + r[2], 0))} eventi geolocalizzati. Area delle bolle: frequenza. Colore: decessi medi per evento. Un riepilogo accessibile dei principali paesi è disponibile sotto la mappa.`}
      />
      {hover && (
        <div className="map-tooltip" role="status">
          <strong>
            {fmt(hover.n)} eventi · {fmt(hover.deaths / hover.n, 2)} decessi/evento
          </strong>
          <span>
            {fmt(hover.lat, 1)}° lat · {fmt(hover.lng, 1)}° lon
          </span>
        </div>
      )}
      {year === 1993 && (
        <div className="map-empty">
          <strong>1993</strong>
          <span>Rilevazioni mancanti</span>
        </div>
      )}
    </div>
  );
}
