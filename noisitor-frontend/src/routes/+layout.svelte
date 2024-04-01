<script>
  import "../style.css";
  import "@picocss/pico/css/pico.conditional.min.css";
  import Header from "./Header.svelte";
</script>

<main>
  <Header />
  <slot />
</main>
