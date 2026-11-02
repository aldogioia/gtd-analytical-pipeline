import { geoContains } from 'd3-geo';
import { feature } from 'topojson-client';
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const topology = JSON.parse(readFileSync(require.resolve('world-atlas/land-110m.json')));
const land = feature(topology, topology.objects.land),
  positions = [];
for (let lat = -82; lat < 85; lat += 1.35) {
  const step = 1.35 / Math.cos((lat * Math.PI) / 180);
  for (let lng = -180; lng < 180; lng += step) {
    if (geoContains(land, [lng, lat])) {
      const p = (lat * Math.PI) / 180,
        t = (lng * Math.PI) / 180;
      positions.push(
        ...[
          1.003 * Math.cos(p) * Math.sin(t),
          1.003 * Math.sin(p),
          1.003 * Math.cos(p) * Math.cos(t),
        ].map((v) => +v.toFixed(5)),
      );
    }
  }
}
writeFileSync(new URL('../src/data/land-points.json', import.meta.url), JSON.stringify(positions));
console.log(
  `${positions.length / 3} land points precomputed; no geographic computation on page load.`,
);
