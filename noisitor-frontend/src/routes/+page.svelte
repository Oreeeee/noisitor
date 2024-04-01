<script>
  export let data;
  import {
    fetchUniqueIPs,
    fetchEventsLogged,
    fetchLastEvents,
  } from "$lib/fetchStats";
  import { onMount } from "svelte";
  import LastEvent from "../components/LastEvent.svelte";
  import Stats from "../components/Stats.svelte";
  import EventsMap from "../components/EventsMap.svelte";

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
    <h3>Statistics:</h3>
    <hr />
    <Stats {uniqueIPs} {eventsLogged} />
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
      {#each lastEvents as event, i}
        {#if i > 0}
          <hr />
        {/if}
        <LastEvent eventData={event} />
      {/each}
    </div>
  </div>
</div>
