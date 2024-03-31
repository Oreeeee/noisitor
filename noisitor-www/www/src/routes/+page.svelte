<script>
  var uniqueIPs = 0;
  var eventsLogged = 0;

  function fetchStats() {
    // TODO: Make this fetching better, maybe fetch one JSON file?
    fetch("/data/unique-ips")
      .then((x) => x.text())
      .then((data) => (uniqueIPs = data));

    fetch("/data/total-events")
      .then((x) => x.text())
      .then((data) => (eventsLogged = data));
  }

  setInterval(fetchStats, 5000);
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
