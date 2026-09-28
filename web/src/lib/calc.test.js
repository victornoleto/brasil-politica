import { describe, expect, it } from 'vitest'
import { coordinate, institutionParties, overallPosition, institutionPosition } from './calc.js'

const parties = {
  PT: { x: -5, y: -2 },
  PL: { x: 5, y: 3, periods: [{ since: 2019, x: 7, y: 6 }] },
}
const composition = {
  presidency: { 2020: { PL: 1 }, 2023: { PT: 1 } },
  chamber: { 2023: { PT: 100, PL: 300, NO_PARTY: 5 } },
}

describe('coordinate', () => {
  it('applies a period from its year on', () => {
    expect(coordinate(parties, 'PL', 2018)).toEqual({ x: 5, y: 3 })
    expect(coordinate(parties, 'PL', 2019)).toEqual({ x: 7, y: 6 })
  })
})

describe('institutionPosition', () => {
  it('seat-weighted mean, skipping parties without a coordinate', () => {
    const p = institutionPosition(composition, parties, 'chamber', 2023)
    expect(p.x).toBeCloseTo((-5 * 100 + 7 * 300) / 400)
    expect(p.noCoord).toBe(5)
  })
})

describe('overallPosition', () => {
  it('only the Presidency weighted => coordinate of the president\'s party', () => {
    const weights = { presidency: 30, chamber: 0 }
    expect(overallPosition(composition, parties, weights, 2023)).toEqual({ x: -5, y: -2 })
  })
  it('renormalizes when an institution is missing in the year', () => {
    const weights = { presidency: 50, chamber: 50 }
    expect(overallPosition(composition, parties, weights, 2020)).toEqual({ x: 7, y: 6 })
  })
})

describe('institutionParties', () => {
  it('lists parties with a coordinate, largest caucus first, without NO_PARTY', () => {
    const list = institutionParties(composition, parties, 'chamber', 2023)
    expect(list.map((p) => p.party)).toEqual(['PL', 'PT'])
    expect(list[0]).toMatchObject({ seats: 300, x: 7, y: 6 })
  })
})
