<script>
  import { toggleTheme, load, store } from './lib/store.svelte.js'
  import Spectrum from './views/Spectrum.svelte'
  import Timeline from './views/Timeline.svelte'
  import Composition from './views/Composition.svelte'
  import Settings from './views/Settings.svelte'
  import Offices from './views/Offices.svelte'
  import Methodology from './views/Methodology.svelte'

  const TABS = [
    { id: 'spectrum', name: 'Espectro', title: 'Espectro político', comp: Spectrum },
    { id: 'timeline', name: 'Linha do tempo', title: 'Linha do tempo', comp: Timeline },
    { id: 'composition', name: 'Composição', title: 'Composição partidária', comp: Composition },
    { id: 'settings', name: 'Pesos e partidos', title: 'Pesos e partidos', comp: Settings },
    { id: 'offices', name: 'Os cargos', title: 'Os cargos', comp: Offices },
    { id: 'methodology', name: 'Metodologia', title: 'Metodologia', comp: Methodology },
  ]
  const STATIC_TABS = ['offices', 'methodology'] // render without the data

  const fromHash = () => TABS.find((a) => a.id === location.hash.slice(1))?.id ?? 'spectrum'
  let tab = $state(fromHash())
  $effect(() => {
    const f = () => (tab = fromHash())
    addEventListener('hashchange', f)
    return () => removeEventListener('hashchange', f)
  })

  let error = $state(null)
  load().catch((e) => (error = e.message))

  const currentTab = $derived(TABS.find((a) => a.id === tab))
  const Current = $derived(currentTab.comp)
</script>

<div class="mx-auto max-w-300 p-4">
  <header class="relative">
    <button class="absolute top-2 right-0" onclick={toggleTheme} aria-label="Alternar tema claro/escuro">
      {store.theme === 'dark' ? '☀ Claro' : '☾ Escuro'}
    </button>
    <h1 class="mt-2 pr-30">Espectro Político do Brasil</h1>
    <p class="mb-3 text-ink-2">1994–2026 · Se o Brasil está ruim, a culpa é só do presidente?</p>
    <nav class="mb-4 flex flex-wrap gap-1 border-b border-line">
      {#each TABS as a}
        <a
          href="#{a.id}"
          class={[
            'border-b-2 px-3 py-2 no-underline',
            tab === a.id ? 'border-accent font-semibold text-ink' : 'border-transparent text-ink-2',
          ]}
          aria-current={tab === a.id ? 'page' : undefined}>{a.name}</a
        >
      {/each}
    </nav>
  </header>

  <main class="min-w-0">
    <h2 class="mb-3">{currentTab.title}</h2>
    {#if error}
      <p class="card">Falha ao carregar dados: {error}</p>
    {:else if !store.composition && !STATIC_TABS.includes(tab)}
      <p class="text-muted">Carregando dados…</p>
    {:else}
      <Current />
    {/if}
  </main>
</div>
