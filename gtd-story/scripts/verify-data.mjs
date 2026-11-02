import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const read = (name) =>
  JSON.parse(readFileSync(new URL(`../public/data/${name}.json`, import.meta.url)));
const d = read('story'),
  locations = read('locations'),
  map = read('map-locations'),
  sum = (rows, key) => rows.reduce((n, r) => n + (r[key] || 0), 0);
assert.equal(d.totals.events, 209706);
assert.equal(d.totals.deaths, 523944);
assert.equal(sum(d.years, 'events'), d.totals.events);
assert.equal(sum(d.years, 'deaths'), d.totals.deaths);
assert.deepEqual(
  d.years.filter((x) => x.events === null).map((x) => x.year),
  [1993],
);
for (const name of ['attacks', 'targets'])
  for (const mode of ['all', 'suicide']) {
    const rows = d[name][mode],
      ref = mode === 'all' ? d.totals : d.suicide.find((x) => x.is_suicide === 1);
    assert.equal(sum(rows, 'events'), ref.events);
    assert.equal(sum(rows, 'deaths'), ref.deaths);
  }
for (const g of d.groups) {
  assert.equal(sum(g.weapons, 'events'), g.events);
  assert.equal(sum(g.weapons, 'deaths'), g.deaths);
}
let pointsTotal = 0;
for (const [year, rows] of Object.entries(locations)) {
  assert(+year >= 1970 && +year <= 2020);
  for (const [lat, lng, count, deaths] of rows) {
    assert(lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180);
    assert(Number.isInteger(count) && count > 0);
    assert(Number.isInteger(deaths) && deaths >= 0);
    pointsTotal += count;
  }
}
assert.equal(pointsTotal, d.totals.geocodedEvents);
let mapEvents = 0,
  mapDeaths = 0;
for (const [year, rows] of Object.entries(map)) {
  assert.equal(
    rows.reduce((s, r) => s + r[2], 0),
    locations[year].reduce((s, r) => s + r[2], 0),
  );
  assert.equal(
    rows.reduce((s, r) => s + r[3], 0),
    locations[year].reduce((s, r) => s + r[3], 0),
  );
  for (const [lat, lng, n, deaths] of rows) {
    assert(Number.isFinite(deaths / n));
    assert(lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180);
    mapEvents += n;
    mapDeaths += deaths;
  }
}
assert.equal(mapEvents, d.totals.geocodedEvents);
assert.equal(mapDeaths, d.totals.geocodedDeaths);

assert.equal(
  d.totals.reportedDeaths +
    sum(
      d.sources.filter((s) => s.nkill_source === 'Imputed'),
      'deaths',
    ),
  d.totals.deaths,
);
console.log(
  'PASS · totals, yearly series, 1993 gap, primary joins, suicide subsets, group weapons, geographic cells, death provenance and complete frequency/lethality encodings.',
);
