<script>
  import SinglePointMap from "./SinglePointMap.svelte";

  export let ip;
  export let geolocation;

  let hasGeolocationData = true;
  if (
    geolocation == null ||
    geolocation.lat == "0.000000" ||
    geolocation.long == "0.000000"
  ) {
    hasGeolocationData = false;
  }
</script>

<div class="grid">
  {#if !hasGeolocationData}
    <center>
      <p>No geolocation data about {ip}</p>
    </center>
  {:else}
    <div class="pico">
      <h1>Geolocation</h1>
      <hr />
      {#each Object.entries(geolocation) as [k, v]}
        <p><strong>{k}</strong>: {v}</p>
      {/each}
    </div>
    <div>
      <div class="pico">
        <h1>Map</h1>
        <hr />
      </div>
      <SinglePointMap lat={geolocation.lat} long={geolocation.long} />
    </div>
  {/if}
</div>
