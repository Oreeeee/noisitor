<script>
  export let ip;
  export let wide;
</script>

<a href="/details/{ip}">
  {#if wide}
    <button class="wide-button">More info</button>
  {:else}
    <button>More info</button>
  {/if}
</a>
