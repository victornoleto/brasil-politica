// Color tokens read from the CSS (light/dark theme) and a diverging scale by economic position.

import { store } from './store.svelte.js'

export function theme() {
  void store.theme // reactive dependency: charts recompute when the theme changes
  const s = getComputedStyle(document.documentElement)
  const v = (n) => s.getPropertyValue(`--color-${n}`).trim()
  return {
    surface: v('surface'),
    ink: v('ink'),
    ink2: v('ink-2'),
    muted: v('muted'),
    grid: v('grid'),
    axis: v('axis'),
    left: v('pole-left'),
    right: v('pole-right'),
    neutral: v('pole-mid'),
    qAuthLeft: v('q-auth-left'),
    qAuthRight: v('q-auth-right'),
    qLibLeft: v('q-lib-left'),
    qLibRight: v('q-lib-right'),
    bubble: v('bubble'),
    bubbleBorder: v('bubble-border'),
    series: [1, 2, 3, 4, 5, 6].map((i) => v(`series-${i}`)),
  }
}

const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16))
const mix = (a, b, t) => {
  const [ra, ga, ba] = hex(a)
  const [rb, gb, bb] = hex(b)
  const c = (x, y) => Math.round(x + (y - x) * t).toString(16).padStart(2, '0')
  return `#${c(ra, rb)}${c(ga, gb)}${c(ba, bb)}`
}

/** x ∈ [-10, 10] → red (left) … gray … blue (right). */
export function colorByX(x, t) {
  const k = Math.max(-1, Math.min(1, x / 10))
  return k < 0 ? mix(t.neutral, t.left, -k) : mix(t.neutral, t.right, k)
}
