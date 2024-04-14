<script>
  export let data;
  import { fetchStats } from "$lib/fetchStats";
  import { onMount } from "svelte";
  import LastEvent from "../components/LastEvent.svelte";
  import Stats from "../components/Stats.svelte";
  import EventsMap from "../components/EventsMap.svelte";

  // Initial data fetch on server
  let stats = data.stats;

  // TODO: Fix mounts and unmounts to stop memory leaks
  onMount(() => {
    // Refresh the data on the client every 5s
    setInterval(() => {
      fetchStats().then((ret) => (stats = ret));
    }, 5000);
  });
</script>

<div class="site-contents grid">
  <div id="left-column" class="pico">
    <h3>Statistics:</h3>
    <hr />
    <Stats {stats} />

    <div>
      <a href="/show-all"
        ><button class="wide-button">Show all events</button></a
      ><br /><br />
      <button class="wide-button">Search the database</button><br /><br />
      <button class="wide-button contrast">More statistics</button>
    </div>
  </div>

  <div id="middle-column">
    <div class="pico">
      <h3>Event sources map:</h3>
      <hr />
    </div>
    <EventsMap />
  </div>

  <div id="right-column" class="pico">
    <h3>Last 50 events:</h3>
    <hr />
    <div id="last-events-container">
      {#each stats.last as event, i}
        {#if i > 0}
          <hr />
        {/if}
        <LastEvent eventData={event} />
      {/each}
    </div>
  </div>
</div>
