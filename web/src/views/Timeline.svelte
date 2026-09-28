<script>
  import Chart from '../lib/Chart.svelte'
  import { INSTITUTIONS, overallPosition, institutionPosition } from '../lib/calc.js'
  import { store, effectiveParties } from '../lib/store.svelte.js'
  import { theme } from '../lib/colors.js'

  const YEARS = Array.from({ length: 2026 - 1994 + 1 }, (_, i) => 1994 + i)
  const parties = $derived(effectiveParties())

  function option(axis) {
    const t = theme()
    const series = (name, color, values, width = 2) => ({
      name, type: 'line', showSymbol: false, connectNulls: false,
      lineStyle: { color, width }, itemStyle: { color },
      endLabel: { show: true, color: t.ink2, formatter: name.split(' ')[0] },
      // [year, value] pairs without the empty years: endLabel animates from the 1st point and breaks if it is null
      data: values.map((v, i) => [String(YEARS[i]), v]).filter(([, v]) => v != null),
    })
    return {
      grid: { left: 40, right: 110, top: 44, bottom: 32 },
      legend: { top: 4, left: 0, textStyle: { color: t.ink2 }, icon: 'roundRect', itemHeight: 3 },
      tooltip: { trigger: 'axis', valueFormatter: (v) => (v == null ? '—' : v.toFixed(1)) },
      xAxis: { type: 'category', data: YEARS, axisLabel: { color: t.muted }, axisLine: { lineStyle: { color: t.axis } } },
      yAxis: { type: 'value', min: -10, max: 10, interval: 5, axisLabel: { color: t.muted }, splitLine: { lineStyle: { color: t.grid } } },
      series: [
        ...INSTITUTIONS.map((i, k) =>
          series(i.name, t.series[k], YEARS.map((y) => institutionPosition(store.composition, parties, i.id, y)?.[axis] ?? null)),
        ),
        series('Brasil (ponderado)', t.ink, YEARS.map((y) => overallPosition(store.composition, parties, store.weights, y)?.[axis] ?? null), 3),
      ],
    }
  }

  const opX = $derived(option('x'))
  const opY = $derived(option('y'))
</script>

<section class="space-y-4">
  <div class="card">
    <h3>Eixo econômico</h3>
    <p class="mb-3 text-sm text-muted">Posição média de cada instituição por ano: −10 esquerda · +10 direita.</p>
    <Chart option={opX} height={340} label="Posição econômica de cada instituição por ano" />
  </div>
  <div class="card">
    <h3>Eixo social</h3>
    <p class="mb-3 text-sm text-muted">Posição média de cada instituição por ano: −10 libertário · +10 autoritário.</p>
    <Chart option={opY} height={340} label="Posição social de cada instituição por ano" />
  </div>
</section>
