// One quantitative scale shared by the geographic and categorical comparisons.
// Values above 10 keep the endpoint color and remain exact in labels/tooltips.
export const severityStops = [
  [0, '#8ba9c1'],
  [2, '#c1bea1'],
  [5, '#e6a365'],
  [10, '#e8694f'],
];
export function severityColor(value) {
  const v = Math.max(0, Number(value) || 0);
  const stop = severityStops.findIndex(([n]) => n >= v);
  if (stop <= 0) return stop === -1 ? severityStops.at(-1)[1] : severityStops[0][1];
  const [a, ca] = severityStops[stop - 1],
    [b, cb] = severityStops[stop];
  const t = (v - a) / (b - a);
  const rgb = [1, 3, 5].map((i) =>
    Math.round(parseInt(ca.slice(i, i + 2), 16) * (1 - t) + parseInt(cb.slice(i, i + 2), 16) * t),
  );
  return `rgb(${rgb.join(',')})`;
}
export const weaponStyles = {
  Explosives: { color: '#dfa55e', label: 'Esplosivi' },
  Firearms: { color: '#7badd2', label: 'Armi da fuoco' },
  Incendiary: { color: '#d17c8c', label: 'Incendiarie' },
  Melee: { color: '#a798d0', label: 'Armi bianche' },
  CBRN: { color: '#78b7a2', label: 'CBRN' },
  Other: { color: '#a0a88a', label: 'Altre armi' },
  Unknown: { color: '#7f8995', label: 'Armi non note' },
};
export function weaponStyle(category) {
  const key = ['Chemical', 'Biological', 'Radiological', 'Nuclear'].includes(category)
    ? 'CBRN'
    : category;
  return weaponStyles[key] || weaponStyles.Other;
}
export const easeOut = [0.23, 1, 0.32, 1];
