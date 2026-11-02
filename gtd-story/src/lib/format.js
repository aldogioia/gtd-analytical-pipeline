export const fmt = (n, d = 0) =>
  new Intl.NumberFormat('it-IT', {
    maximumFractionDigits: d,
    minimumFractionDigits: d,
    useGrouping: 'always',
  }).format(n);
