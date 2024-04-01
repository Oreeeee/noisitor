<script>
  export let data;
  import {
    fetchUniqueIPs,
    fetchEventsLogged,
    fetchLastEvents,
  } from "$lib/fetchStats";
  import { onMount } from "svelte";
  import LastEvent from "../components/LastEvent.svelte";

  // Initial data fetch on server
  var uniqueIPs = data.uniqueIPs;
  var eventsLogged = data.eventsLogged;
  var lastEvents = data.lastEvents;

  onMount(() => {
    // Refresh the data on the client every 5s
    setInterval(() => {
      fetchUniqueIPs().then((ret) => (uniqueIPs = ret));
      fetchEventsLogged().then((ret) => (eventsLogged = ret));
      fetchLastEvents().then((ret) => (lastEvents = ret));
    }, 5000);
  });
</script>

<div id="app-grid" class="grid">
  <div id="left-column" class="pico">
    <p>Unique IPs logged:</p>
    <h1>{uniqueIPs}</h1>
    <br />
    <p>Events logged:</p>
    <h1>{eventsLogged}</h1>
    <br />
  </div>

  <div id="middle-column">
    <div id="ip-map"></div>
  </div>

  <div id="right-column" class="pico">
    <p>Last 50 events:</p>
    <div id="last-events-container">
      {#each lastEvents as event, i}
        {#if i > 0}
          <hr />
        {/if}
        <LastEvent eventData={event} />
      {/each}
    </div>
  </div>
</div>
