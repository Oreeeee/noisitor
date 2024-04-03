<script>
  export let ip;
  export let wide;
</script>

<a href="https://abuseipdb.com/check/{ip}" target="_blank">
  {#if wide}
    <button class="wide-button secondary">AbuseIPDB</button>
  {:else}
    <button class="secondary">AbuseIPDB</button>
  {/if}
</a>
