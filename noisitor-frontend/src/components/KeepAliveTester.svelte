<script>
  var alive = true;

  import { onMount } from "svelte";

  onMount(() => {
    setInterval(() => {
      alive = true;
      fetch("/data/keepalive").catch(() => {
        alive = false;
      });
    }, 10000);
  });
</script>

{#if !alive}
  <p>⚠️ Lost connection to server!</p>
{/if}
