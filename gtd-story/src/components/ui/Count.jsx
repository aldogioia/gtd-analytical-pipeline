import { useRef, useEffect } from 'react';
import { useInView, useReducedMotion, animate } from 'framer-motion';
import { fmt } from '../../lib/format';
export default function Count({ value, decimals = 0, suffix = '' }) {
  const ref = useRef(),
    inView = useInView(ref, { once: true }),
    reduce = useReducedMotion();
  useEffect(() => {
    if (!inView) return;
    if (reduce) {
      ref.current.textContent = fmt(value, decimals) + suffix;
      return;
    }
    const controls = animate(0, value, {
      duration: 1.5,
      ease: [0.23, 1, 0.32, 1],
      onUpdate: (v) => {
        if (ref.current)
          ref.current.textContent =
            fmt(Math.round(v * 10 ** decimals) / 10 ** decimals, decimals) + suffix;
      },
    });
    return () => controls.stop();
  }, [value, inView, reduce, decimals, suffix]);
  return (
    <span ref={ref}>
      {fmt(value, decimals)}
      {suffix}
    </span>
  );
}
