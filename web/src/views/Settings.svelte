<script>
  import { INSTITUTIONS, coordinate } from '../lib/calc.js'
  import { store, resetCoords, resetWeights, save } from '../lib/store.svelte.js'
  import PartyEditor from '../lib/PartyEditor.svelte'
  import Chart from '../lib/Chart.svelte'
  import YearSlider from '../lib/YearSlider.svelte'
  import { compassOption } from '../lib/compass.js'
  import { theme } from '../lib/colors.js'

  let onlyWithSeats = $state(true)

  const weightSum = $derived(INSTITUTIONS.reduce((s, i) => s + (store.weights[i.id] || 0), 0))
  const list = $derived(
    Object.entries(store.baseParties ?? {}).sort(([, a], [, b]) => a.x - b.x),
  )

  const currentCoord = (id) => store.editedCoords[id] ?? coordinate(store.baseParties, id, store.year)

  function edit(id, axis, value) {
    if (value === '' || Number.isNaN(Number(value))) return // incomplete input (e.g. just "-")
    store.editedCoords[id] = { ...currentCoord(id), [axis]: Math.max(-10, Math.min(10, Number(value))) }
    save()
  }

  // Floating mini-spectrum next to the row being edited
  const PREVIEW_WIDTH = 360
  let fineTune
  let preview = $state(null) // { id, top, left } or { id, fixed: true }

  function showPreview(id, e) {
    const row = e.currentTarget.closest('tr')
    const base = fineTune.getBoundingClientRect()
    // right after the last column (Social), vertically centered on the row
    const left = row.lastElementChild.getBoundingClientRect().right - base.left + 16
    if (fineTune.clientWidth - left < PREVIEW_WIDTH) {
      preview = { id, fixed: true } // no room beside it (phone): bottom corner of the screen
    } else {
      const top = Math.max(0, row.getBoundingClientRect().top - base.top + row.offsetHeight / 2 - PREVIEW_WIDTH / 2)
      preview = { id, top, left }
    }
  }

  function hidePreview(e) {
    if (!e.currentTarget.contains(e.relatedTarget)) preview = null
  }

  const previewOption = $derived.by(() => {
    if (!preview) return null
    const t = theme()
    const c = currentCoord(preview.id)
    const others = Object.keys(store.baseParties ?? {})
      .filter((id) => id !== preview.id)
      .map((id) => ({ ...currentCoord(id), value: 0, label: id, detail: 'outro partido' }))
    return compassOption({
      t, compact: true, margin: 56, maxLabels: 0, bubbles: others,
      means: [{ name: preview.id, label: preview.id, x: c.x, y: c.y, color: t.series[0], symbol: 'circle', fixedSize: 16 }],
    })
  })
</script>

<section class="space-y-4">
  <div class="card">
    <h3>Peso de cada instituição</h3>
    <p class="mb-3 text-muted">
      Quanto cada instituição influencia a vida do cidadão. O peso é dividido igualmente entre os membros da
      instituição. Os pesos são relativos: o app normaliza para 100%.
    </p>
    {#each INSTITUTIONS as i}
      <label class="my-1.5 grid grid-cols-[1fr_48px] items-center gap-3 min-[601px]:grid-cols-[200px_1fr_48px]">
        <span>{i.name}</span>
        <input type="range" min="0" max="100" bind:value={store.weights[i.id]} onchange={save} class="max-[600px]:col-span-full" />
        <strong>{weightSum ? Math.round((100 * store.weights[i.id]) / weightSum) : 0}%</strong>
      </label>
    {/each}
    <button class="mt-3" onclick={resetWeights}>Restaurar pesos padrão</button>
  </div>

  <div class="card">
    <h3>Coordenadas dos partidos</h3>
    <p class="mb-3 text-muted">
      <b>Arraste cada partido</b> para a posição que você considera correta. Os valores iniciais são
      <b>estimativas</b>. Um partido editado fica azul e mantém a posição em todos os anos,
      substituindo as mudanças de perfil por período. Mostrando posições de {store.year}; o tamanho indica as
      cadeiras na Câmara.
    </p>
    <div class="mb-3 flex flex-wrap items-center gap-4">
      <YearSlider />
      <label class="flex items-center gap-2"><input type="checkbox" bind:checked={onlyWithSeats} /> só partidos com cadeiras no Congresso</label>
      <button onclick={resetCoords}>Restaurar coordenadas padrão</button>
    </div>
    <PartyEditor {onlyWithSeats} />
    <h4 class="mt-5 mb-3">Ajuste fino</h4>
    <p class="mb-2 text-muted">
      Cada partido tem duas coordenadas, de <b>−10 a +10</b>, em passos de 0,5. O zero é o centro.
    </p>
    <ul class="mb-2 list-disc pl-4.5">
      <li><b>Econômico:</b> −10 = extrema esquerda (mais Estado na economia) · +10 = extrema direita (mais mercado).</li>
      <li><b>Social:</b> −10 = totalmente libertário (mais liberdade individual) · +10 = totalmente autoritário (mais ordem e controle).</li>
    </ul>
    <p class="text-sm text-muted">Ao editar um campo, um mini-espectro mostra onde o partido fica.</p>
    <div class="relative" bind:this={fineTune}>
    <table class="mt-3 block overflow-x-auto">
      <thead><tr><th>Sigla</th><th>Nome</th><th>Econômico</th><th>Social</th></tr></thead>
      <tbody>
        {#each list as [id, p]}
          {@const c = store.editedCoords[id] ?? coordinate(store.baseParties, id, store.year)}
          {@const edited = !!store.editedCoords[id]}
          <tr
            class={preview?.id === id && '[&>td]:bg-page'}
            onfocusin={(e) => showPreview(id, e)}
            onfocusout={hidePreview}
          >
            <td class={edited && 'font-bold text-accent'}>{id}</td>
            <td>{p.name}{p.periods?.length && !edited ? ' *' : ''}</td>
            {#each ['x', 'y'] as axis}
              <td>
                <input
                  type="number" step="0.5" min="-10" max="10" value={c[axis]}
                  class="w-18 rounded border border-line bg-page px-1 py-0.5 text-ink"
                  aria-label="{id}: posição {axis === 'x' ? 'econômica' : 'social'}"
                  oninput={(e) => edit(id, axis, e.target.value)}
                />
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
    {#if preview && previewOption}
      <div
        class={[
          'card pointer-events-none z-10 p-2 shadow-[0_8px_24px_rgba(0,0,0,0.15)]',
          preview.fixed ? 'fixed right-4 bottom-4 w-60' : 'absolute w-90',
        ]}
        style={preview.fixed ? '' : `top:${preview.top}px;left:${preview.left}px`}
        aria-hidden="true"
      >
        <Chart option={previewOption} height={PREVIEW_WIDTH - 18} square label="Posição de {preview.id}" />
      </div>
    {/if}
    </div>
    <p class="mt-3 text-sm text-muted">* posição muda ao longo do tempo (ex.: PSL antes/depois de 2018).</p>
  </div>
</section>
