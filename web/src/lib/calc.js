// Position on the spectrum. Data: composition[inst][year][party] = seat-equivalents.

export const INSTITUTIONS = [
  { id: 'presidency', name: 'Presidência', defaultWeight: 30 },
  { id: 'chamber', name: 'Câmara dos Deputados', defaultWeight: 25 },
  { id: 'senate', name: 'Senado', defaultWeight: 20 },
  { id: 'governors', name: 'Governadores', defaultWeight: 15 },
  { id: 'assemblies', name: 'Assembleias Legislativas', defaultWeight: 10 },
]

/** Party coordinate in the year, applying `periods` (the last one with since <= year wins). */
export function coordinate(parties, id, year) {
  const p = parties[id]
  if (!p) return null
  let c = { x: p.x, y: p.y }
  for (const per of [...(p.periods ?? [])].sort((a, b) => a.since - b.since)) {
    if (per.since <= year) c = { x: per.x, y: per.y }
  }
  return c
}

/** Parties of an institution in the year, with coordinate and seats, largest first. */
export function institutionParties(composition, parties, inst, year) {
  const comp = composition[inst]?.[year] ?? {}
  return Object.entries(comp)
    .map(([party, seats]) => ({ party, seats, ...coordinate(parties, party, year) }))
    .filter((p) => p.x !== undefined)
    .sort((a, b) => b.seats - a.seats)
}

/** Mean coordinates of an institution in a year, weighted by seats. Skips parties without a coordinate. */
export function institutionPosition(composition, parties, inst, year) {
  const comp = composition[inst]?.[year]
  if (!comp) return null
  let x = 0, y = 0, total = 0, noCoord = 0
  for (const [party, seats] of Object.entries(comp)) {
    const c = coordinate(parties, party, year)
    if (!c) { noCoord += seats; continue }
    x += c.x * seats
    y += c.y * seats
    total += seats
  }
  if (total === 0) return null
  return { x: x / total, y: y / total, seats: total, noCoord }
}

/** Overall position: mean of the institutions weighted by the weights, renormalized among those with data in the year. */
export function overallPosition(composition, parties, weights, year) {
  let x = 0, y = 0, sum = 0
  for (const { id } of INSTITUTIONS) {
    const weight = weights[id] ?? 0
    const pos = weight > 0 && institutionPosition(composition, parties, id, year)
    if (!pos) continue
    x += pos.x * weight
    y += pos.y * weight
    sum += weight
  }
  return sum === 0 ? null : { x: x / sum, y: y / sum }
}
