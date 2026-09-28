<script>
  import echarts, { withFont } from './echarts.js'

  let { option, height = 420, label, square = false } = $props()
  let el
  let chart = $state(null)

  $effect(() => {
    const c = echarts.init(el, null, { renderer: 'svg' })
    chart = c
    const ro = new ResizeObserver(() => c.resize())
    ro.observe(el)
    return () => {
      ro.disconnect()
      c.dispose()
    }
  })

  $effect(() => {
    chart?.setOption(withFont(option), true)
  })
</script>

<div
  bind:this={el}
  role="img"
  aria-label={label}
  class={['w-full', square && 'mx-auto aspect-square']}
  style={square ? `max-width:${height}px` : `height:${height}px`}
></div>
