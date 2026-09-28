import { FONT } from './echarts.js'

// ECharts option for the political plane in quadrants ("political compass" style).
//   bubbles: [{ label, detail, x, y, value }]   — area ∝ value (e.g. the party's seats)
//   means:   [{ name, x, y, weight, color, symbol }] — area ∝ weight set by the user

const fmt = (v) => (v >= 0 ? '+' : '') + v.toFixed(1)

/** Diameter with area proportional to the value. */
const diameter = (v, max, min, maxD) => (max > 0 ? min + (maxD - min) * Math.sqrt(v / max) : min)

/** Label to the right; if an earlier point is closer than 2 units, cycle to bottom/top/left. */
function labelPosition(means, i) {
  const m = means[i]
  const neighbors = means.slice(0, i).filter((o) => Math.hypot(o.x - m.x, o.y - m.y) < 2).length
  const base = m.x > 5 ? 'left' : 'right'
  return [base, 'bottom', 'top', base === 'left' ? 'right' : 'left'][neighbors % 4]
}

export function compassOption({ t, bubbles = [], means = [], compact = false, maxLabels = 12, margin: fixedMargin }) {
  const maxValue = Math.max(0, ...bubbles.map((b) => b.value))
  const maxWeight = Math.max(0, ...means.map((m) => m.weight ?? 0))
  const bubbleD = compact ? 44 : 60
  // equal margins on all 4 sides: in a square container the plot area (and each quadrant) stays 1:1
  const margin = fixedMargin ?? (compact ? 58 : 64)
  const axis = () => ({
    type: 'value', min: -10, max: 10, interval: 5,
    axisLine: { show: false }, axisTick: { show: false },
    axisLabel: { show: false }, splitLine: { show: false },
  })
  // labels at the ends of the axes, as in the political compass
  const end = (text, pos) => ({
    type: 'text', id: `end-${text}`, silent: true, ...pos,
    style: { text, fill: t.ink2, fontSize: compact ? 11 : 12, fontWeight: 500, fontFamily: FONT },
  })

  return {
    animationDurationUpdate: 400,
    grid: { left: margin, right: margin, top: margin, bottom: margin },
    xAxis: axis(),
    yAxis: axis(),
    graphic: [
      end('Autoritária', { left: 'center', top: margin - 20 }),
      end('Libertária', { left: 'center', bottom: margin - 20 }),
      end('Esquerda', { left: 2, top: 'middle' }),
      end('Direita', { right: 2, top: 'middle' }),
    ],
    tooltip: {
      trigger: 'item',
      formatter: (p) => p.data?.tip ?? '',
    },
    series: [
      {
        // quadrants + central axes
        type: 'scatter', data: [], silent: true,
        markArea: {
          silent: true,
          data: [
            [{ coord: [-10, 0], itemStyle: { color: t.qAuthLeft } }, { coord: [0, 10] }],
            [{ coord: [0, 0], itemStyle: { color: t.qAuthRight } }, { coord: [10, 10] }],
            [{ coord: [-10, -10], itemStyle: { color: t.qLibLeft } }, { coord: [0, 0] }],
            [{ coord: [0, -10], itemStyle: { color: t.qLibRight } }, { coord: [10, 0] }],
          ],
        },
        markLine: {
          silent: true, symbol: 'none', label: { show: false },
          lineStyle: { color: t.axis, type: 'solid', width: 1 },
          data: [{ xAxis: 0 }, { yAxis: 0 }],
        },
      },
      bubbles.length > 0 && {
        name: 'Partidos', type: 'scatter', z: 3,
        itemStyle: { color: t.bubble, borderColor: t.bubbleBorder, borderWidth: 1.5, opacity: 0.9 },
        emphasis: { itemStyle: { borderColor: t.ink, borderWidth: 2 } },
        labelLayout: { hideOverlap: true },
        data: bubbles.map((b, i) => ({
          value: [b.x, b.y],
          symbolSize: diameter(b.value, maxValue, 6, bubbleD),
          tip: `<b>${b.label}</b> · ${b.detail}<br>econ. ${fmt(b.x)} · social ${fmt(b.y)}`,
          label: {
            show: i < maxLabels, position: 'top', distance: 4,
            formatter: b.shortLabel ?? b.label, color: t.ink2, fontSize: compact ? 10 : 11,
          },
        })),
      },
      ...means.map((m, i) => ({
        id: m.name, name: m.name, type: 'scatter', // stable id: the point slides between years instead of reappearing
        z: 5, symbol: m.symbol ?? 'diamond',
        itemStyle: { color: m.color, borderColor: t.surface, borderWidth: 2 },
        data: [{
          value: [m.x, m.y],
          symbolSize: m.fixedSize ?? diameter(m.weight, maxWeight, 10, compact ? 30 : 44),
          tip: `<b>${fmt(m.x)}, ${fmt(m.y)}</b><br>${m.name}${m.weight != null ? ` · peso ${m.weightPct}%` : ''}`,
          label: {
            show: true, position: labelPosition(means, i), distance: 6,
            formatter: m.label ?? m.name, color: t.ink, fontWeight: 'bold', fontSize: compact ? 11 : 12,
          },
        }],
      })),
    ].filter(Boolean),
  }
}
