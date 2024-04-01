<script>
  export let data;
  import { fetchUniqueIPs, fetchEventsLogged } from "$lib/fetchStats";

  var uniqueIPs = data.uniqueIPs;
  var eventsLogged = data.eventsLogged;

  setInterval(() => {
    fetchUniqueIPs().then((ret) => (uniqueIPs = ret));
    fetchEventsLogged().then((ret) => (eventsLogged = ret));
  }, 5000);
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
    <div id="last-events-container"></div>
  </div>
</div>
