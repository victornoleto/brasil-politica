<script>
  import Chart from '../lib/Chart.svelte'
  import YearSlider from '../lib/YearSlider.svelte'
  import { INSTITUTIONS, institutionParties, overallPosition, institutionPosition } from '../lib/calc.js'
  import { store, effectiveParties } from '../lib/store.svelte.js'
  import { theme } from '../lib/colors.js'
  import { compassOption } from '../lib/compass.js'

  const SYMBOLS = ['diamond', 'circle', 'rect', 'triangle', 'roundRect']
  const UNIT = { chamber: 'cadeiras', senate: 'cadeiras', governors: 'governadores', assemblies: 'deputados' }
  const fmt = (v) => (v >= 0 ? '+' : '') + v.toFixed(1)

  let playing = $state(false)
  $effect(() => {
    if (!playing) return
    const id = setInterval(() => {
      store.year = store.year >= 2026 ? 1994 : store.year + 1
    }, 900)
    return () => clearInterval(id)
  })

  const parties = $derived(effectiveParties())
  const weightSum = $derived(INSTITUTIONS.reduce((s, i) => s + (store.weights[i.id] || 0), 0))
  const weightPct = (id) => (weightSum ? Math.round((100 * (store.weights[id] || 0)) / weightSum) : 0)

  const overall = $derived(overallPosition(store.composition, parties, store.weights, store.year))
  const byInst = $derived(
    INSTITUTIONS.map((i, k) => ({
      ...i, k,
      pos: institutionPosition(store.composition, parties, i.id, store.year),
      parties: institutionParties(store.composition, parties, i.id, store.year),
    })),
  )
  const congress = $derived.by(() => {
    // Chamber + Senate together, weighted by the user's weights
    const c = byInst.filter((i) => ['chamber', 'senate'].includes(i.id) && i.pos)
    const w = c.reduce((s, i) => s + (store.weights[i.id] || 0), 0)
    if (!w) return null
    return {
      x: c.reduce((s, i) => s + i.pos.x * (store.weights[i.id] || 0), 0) / w,
      y: c.reduce((s, i) => s + i.pos.y * (store.weights[i.id] || 0), 0) / w,
    }
  })

  function meanOf(i, t) {
    return {
      name: i.name, label: i.name.split(' ')[0], x: i.pos.x, y: i.pos.y,
      weight: store.weights[i.id] || 0, weightPct: weightPct(i.id), color: t.series[i.k], symbol: SYMBOLS[i.k],
    }
  }

  // Final spectrum: mean point of each institution (size = weight) + Brazil
  const finalOption = $derived.by(() => {
    const t = theme()
    const means = byInst.filter((i) => i.pos && store.weights[i.id] > 0).map((i) => meanOf(i, t))
    if (overall) {
      means.push({ name: 'Brasil', label: `Brasil ${store.year}`, x: overall.x, y: overall.y, color: t.ink, symbol: 'circle', fixedSize: 22 })
    }
    return compassOption({ t, means })
  })

  // One spectrum per office: parties (size = seats) + mean point (size = weight)
  const officeOptions = $derived.by(() => {
    const t = theme()
    return Object.fromEntries(
      byInst.filter((i) => i.pos).map((i) => {
        const presid = i.id === 'presidency'
        const bubbles = i.parties.map((p) => ({
          x: p.x, y: p.y, value: p.seats,
          label: p.party,
          shortLabel: presid ? p.party : `${p.party} ${Math.round(p.seats)}`,
          detail: presid ? `${Math.round(100 * p.seats)}% do ano` : `${p.seats.toFixed(1)} ${UNIT[i.id]}`,
        }))
        return [i.id, compassOption({ t, bubbles, means: [{ ...meanOf(i, t), label: 'média' }], compact: true })]
      }),
    )
  })
</script>

{#snippet swatch(k)}
  <span class="mr-1.5 inline-block size-2.5 rounded-xs" style="background:var(--color-series-{k + 1})"></span>
{/snippet}

<section>
  <div class="mb-3 flex flex-wrap items-center gap-4">
    <button onclick={() => (playing = !playing)} aria-pressed={playing}>{playing ? '⏸ Pausar' : '▶ Animar'}</button>
    <YearSlider />
  </div>

  <div class="grid gap-4 min-[861px]:grid-cols-[minmax(0,1fr)_340px]">
    <div class="card">
      <h3>Espectro final · {store.year}</h3>
      <p class="mb-3 text-sm text-muted">Ponto médio de cada instituição (tamanho = peso) e o resultado ponderado do Brasil no ano.</p>
      <Chart option={finalOption} height={600} square label="Espectro final: pontos médios das instituições e do Brasil no ano" />
    </div>

    <aside class="card space-y-3">
      <h3>Resumo · {store.year}</h3>
      {#if overall}
        <p class="text-[1.05rem]">Brasil: <b>{fmt(overall.x)}</b> econômico, <b>{fmt(overall.y)}</b> social</p>
      {/if}
      {#if byInst[0].pos && congress}
        <p>
          Distância entre <b>Presidência</b> e <b>Congresso</b> no eixo econômico:
          <b>{Math.abs(byInst[0].pos.x - congress.x).toFixed(1)}</b> pontos
          (Presidência {fmt(byInst[0].pos.x)} × Congresso {fmt(congress.x)}).
        </p>
      {/if}
      <table>
        <thead><tr><th>Instituição</th><th>Econ.</th><th>Social</th><th>Peso</th></tr></thead>
        <tbody>
          {#each byInst as i}
            <tr>
              <td>{@render swatch(i.k)}{i.name}</td>
              {#if i.pos}
                <td>{fmt(i.pos.x)}</td><td>{fmt(i.pos.y)}</td>
              {:else}
                <td colspan="2" class="text-muted">sem dados</td>
              {/if}
              <td>{weightPct(i.id)}%</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <p class="text-sm text-muted">Coordenadas dos partidos são estimativas editáveis. Ver <a href="#methodology">Metodologia</a>.</p>
    </aside>
  </div>

  <p class="mt-6 mb-3 text-ink-2">
    <b>Por cargo · {store.year}.</b> Cada bolinha é um partido (tamanho = cadeiras). O símbolo colorido é a média do cargo (tamanho = peso).
    Discorda da posição de algum partido? <a href="#settings">Arraste-o para outro lugar</a>.
  </p>
  <div class="grid grid-cols-[repeat(auto-fill,minmax(min(100%,440px),1fr))] gap-4">
    {#each byInst as i}
      <article class="card">
        <h3>{@render swatch(i.k)}{i.name}</h3>
        {#if i.pos}
          <p class="mb-3 text-sm text-muted">
            {#if i.id !== 'presidency'}{Math.round(i.pos.seats)} {UNIT[i.id]} · {/if}média {fmt(i.pos.x)}, {fmt(i.pos.y)} · peso {weightPct(i.id)}%
          </p>
          <Chart option={officeOptions[i.id]} height={520} square label="Partidos de {i.name} no espectro em {store.year}" />
        {:else}
          <p class="grid aspect-square max-h-105 w-full place-items-center text-center text-muted">
            Sem dados para {store.year}. {#if ['governors', 'assemblies'].includes(i.id)} O mandato vigente veio da eleição de 1990, fora do recorte.{/if}
          </p>
        {/if}
      </article>
    {/each}
  </div>
</section>
