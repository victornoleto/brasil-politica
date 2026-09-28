import { INSTITUTIONS } from './calc.js'

const DEFAULT_WEIGHTS = Object.fromEntries(INSTITUTIONS.map((i) => [i.id, i.defaultWeight]))

function read(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) ?? fallback
  } catch {
    return fallback
  }
}

export const store = $state({
  composition: null,
  baseParties: null,
  weights: read('weights', { ...DEFAULT_WEIGHTS }),
  // user edits: {PARTY: {x, y}} — apply to every year (ignore `periods`)
  editedCoords: read('editedCoords', {}),
  year: 2025,
  theme: document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light',
})

/** Toggles light/dark: applies it to <html> before changing the state, so the charts read the new colors. */
export function toggleTheme() {
  const next = store.theme === 'dark' ? 'light' : 'dark'
  if (next === 'dark') document.documentElement.dataset.theme = 'dark'
  else delete document.documentElement.dataset.theme
  store.theme = next
  try {
    localStorage.setItem('theme', next)
  } catch {
    /* no storage: applies to this visit only */
  }
}

export function save() {
  try {
    localStorage.setItem('weights', JSON.stringify(store.weights))
    localStorage.setItem('editedCoords', JSON.stringify(store.editedCoords))
  } catch {
    /* storage unavailable: keep it in memory only */
  }
}

export function resetWeights() {
  store.weights = { ...DEFAULT_WEIGHTS }
  save()
}

export function resetCoords() {
  store.editedCoords = {}
  save()
}

/** Effective parties: base + user edits. */
export function effectiveParties() {
  const base = store.baseParties ?? {}
  const out = {}
  for (const [id, p] of Object.entries(base)) {
    const ed = store.editedCoords[id]
    out[id] = ed ? { ...p, x: ed.x, y: ed.y, periods: [] } : p
  }
  return out
}

export async function load() {
  const [composition, parties] = await Promise.all([
    fetch('data/composition.json', { cache: 'no-cache' }).then((r) => r.json()),
    fetch('data/parties.json', { cache: 'no-cache' }).then((r) => r.json()),
  ])
  store.composition = composition
  store.baseParties = parties
}
