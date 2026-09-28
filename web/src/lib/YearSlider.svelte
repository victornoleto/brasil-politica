<script>
  import { store } from './store.svelte.js'
</script>

<label class="flex items-center gap-2">
  Ano <strong>{store.year}</strong>
  <input type="range" min="1994" max="2026" bind:value={store.year} class="w-[min(420px,60vw)]" />
</label>
