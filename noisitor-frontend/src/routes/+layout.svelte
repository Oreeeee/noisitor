<script>
  import "../style.css";
  import "@picocss/pico/css/pico.conditional.min.css";
  import Header from "../components/Header.svelte";
</script>

<main>
  <Header />
  <hr />
  <slot />
</main>
