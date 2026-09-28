<script>
  import Chart from '../lib/Chart.svelte'
  import YearSlider from '../lib/YearSlider.svelte'
  import { INSTITUTIONS, coordinate } from '../lib/calc.js'
  import { store, effectiveParties } from '../lib/store.svelte.js'
  import { colorByX, theme } from '../lib/colors.js'

  const LABELS = { NO_PARTY: 'Sem partido' }
  const parties = $derived(effectiveParties())

  // One 100% bar per institution; segments = parties sorted from left to right.
  const option = $derived.by(() => {
    const t = theme()
    const insts = INSTITUTIONS.filter((i) => store.composition?.[i.id]?.[store.year])
    const rows = insts.map((i) => {
      const comp = store.composition[i.id][store.year]
      const total = Object.values(comp).reduce((s, v) => s + v, 0)
      return Object.entries(comp)
        .map(([p, v]) => ({ p: LABELS[p] ?? p, v, pct: (100 * v) / total, x: coordinate(parties, p, store.year)?.x ?? null }))
        .sort((a, b) => (a.x ?? 99) - (b.x ?? 99))
    })
    const segments = rows.flatMap((l, row) => l.map((s) => ({ ...s, row })))
    return {
      grid: { left: 170, right: 24, top: 8, bottom: 28 },
      tooltip: {
        trigger: 'item',
        formatter: (p) => {
          const s = p.data.s
          return `<b>${s.pct.toFixed(1)}%</b> · ${s.v.toFixed(1)} cadeiras<br>${s.p}${s.x == null ? ' (sem coordenada)' : ` · econ. ${s.x.toFixed(1)}`}`
        },
      },
      xAxis: { type: 'value', max: 100, axisLabel: { color: t.muted, formatter: '{value}%' }, splitLine: { lineStyle: { color: t.grid } } },
      yAxis: { type: 'category', data: insts.map((i) => i.name), inverse: true, axisLabel: { color: t.ink2 }, axisLine: { show: false }, axisTick: { show: false } },
      series: segments.map((s) => ({
        type: 'bar', stack: 'total', barWidth: 28,
        itemStyle: { color: s.x == null ? t.grid : colorByX(s.x, t), borderColor: t.surface, borderWidth: 1 },
        label: { show: s.pct >= 6, color: t.ink, formatter: s.p, fontSize: 11 },
        data: insts.map((_, row) => (row === s.row ? { value: s.pct, s } : null)),
      })),
    }
  })
</script>

<section>
  <div class="mb-3 flex flex-wrap items-center gap-4">
    <YearSlider />
  </div>
  <div class="card">
    <h3>Composição partidária · {store.year}</h3>
    <p class="mb-3 text-sm text-muted">Participação de cada partido em cada instituição, ordenada da esquerda para a direita.</p>
    <Chart {option} height={320} label="Composição partidária de cada instituição no ano selecionado" />
    <div class="flex flex-wrap items-center gap-2 text-sm text-ink-2">
      <span>esquerda</span>
      <span class="h-2 w-40 rounded bg-linear-to-r from-pole-left via-pole-mid to-pole-right"></span>
      <span>direita</span>
      <span class="text-muted">· cor = posição econômica do partido · cinza claro = sem coordenada</span>
    </div>
  </div>
</section>
