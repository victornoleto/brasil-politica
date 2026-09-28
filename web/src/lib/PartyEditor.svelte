<script>
  // Quadrant plane with draggable parties. On drop, writes to store.editedCoords.
  import echarts, { withFont } from './echarts.js'
  import { coordinate } from './calc.js'
  import { store, save } from './store.svelte.js'
  import { theme } from './colors.js'
  import { compassOption } from './compass.js'

  let { onlyWithSeats = true } = $props()

  let el
  let chart = $state(null)

  const step = (v) => Math.max(-10, Math.min(10, Math.round(v * 2) / 2))
  const fmt = (v) => (v >= 0 ? '+' : '') + v.toFixed(1)

  const chamberSeats = $derived(store.composition?.chamber?.[store.year] ?? {})
  const points = $derived(
    Object.keys(store.baseParties ?? {})
      .filter((id) => !onlyWithSeats || chamberSeats[id] > 0 || store.composition?.senate?.[store.year]?.[id] > 0)
      .map((id) => ({
        id,
        edited: !!store.editedCoords[id],
        seats: chamberSeats[id] ?? 0,
        ...(store.editedCoords[id] ?? coordinate(store.baseParties, id, store.year)),
      })),
  )

  function seriesData(list, t) {
    const max = Math.max(1, ...list.map((p) => p.seats))
    return list.map((p) => ({
      value: [p.x, p.y],
      symbolSize: 12 + 30 * Math.sqrt(p.seats / max),
      itemStyle: { color: p.edited ? t.series[0] : t.bubble, borderColor: p.edited ? t.surface : t.bubbleBorder, borderWidth: 1.5 },
      tip: `<b>${p.id}</b> · ${fmt(p.x)}, ${fmt(p.y)}${p.seats ? ` · ${Math.round(p.seats)} dep.` : ''}`,
      label: { show: true, position: 'top', formatter: p.id, color: p.edited ? t.ink : t.ink2, fontSize: 11 },
    }))
  }

  // working copy used while dragging (does not trigger Svelte on every move)
  let list = []
  let dragging = -1

  function draw() {
    if (!chart) return
    const t = theme()
    list = points.map((p) => ({ ...p }))
    const op = compassOption({ t })
    op.series.push({ id: 'parties', type: 'scatter', z: 5, data: seriesData(list, t) })
    chart.setOption(withFont(op), true)
  }

  const local = (e) => {
    const r = el.getBoundingClientRect()
    return [e.clientX - r.left, e.clientY - r.top]
  }

  function press(e) {
    const [px, py] = local(e)
    let best = -1, dist = 24 // capture radius in px
    list.forEach((p, i) => {
      const [x, y] = chart.convertToPixel('grid', [p.x, p.y])
      const d = Math.hypot(x - px, y - py)
      if (d <= dist) { dist = d; best = i } // tie: the topmost one (drawn last)
    })
    if (best < 0) return
    dragging = best
    el.setPointerCapture(e.pointerId)
    e.preventDefault()
  }

  function move(e) {
    if (dragging < 0) {
      el.style.cursor = near(e) ? 'grab' : ''
      return
    }
    const [x, y] = chart.convertFromPixel('grid', local(e))
    list[dragging] = { ...list[dragging], x: step(x), y: step(y), edited: true }
    chart.setOption({ series: [{ id: 'parties', data: seriesData(list, theme()) }] })
  }

  function release() {
    if (dragging < 0) return
    const p = list[dragging]
    dragging = -1
    store.editedCoords[p.id] = { x: p.x, y: p.y }
    save()
  }

  function near(e) {
    const [px, py] = local(e)
    return list.some((p) => {
      const [x, y] = chart.convertToPixel('grid', [p.x, p.y])
      return Math.hypot(x - px, y - py) < 24
    })
  }

  $effect(() => {
    const c = echarts.init(el, null, { renderer: 'svg' })
    chart = c
    const ro = new ResizeObserver(() => {
      c.resize()
      draw()
    })
    ro.observe(el)
    return () => {
      ro.disconnect()
      c.dispose()
    }
  })

  $effect(() => {
    void points // redraw when the year, the filter or the coordinates change
    draw()
  })
</script>

<div
  bind:this={el}
  class="mx-auto aspect-square w-full max-w-160 touch-none"
  onpointerdown={press}
  onpointermove={move}
  onpointerup={release}
  onpointercancel={release}
  role="application" aria-label="Plano político com partidos arrastáveis. Use a tabela abaixo para editar pelo teclado."></div>
