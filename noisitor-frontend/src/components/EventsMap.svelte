<script>
  import "leaflet/dist/leaflet.css";
  import "leaflet.markercluster/dist/MarkerCluster.css";
  import "leaflet.markercluster/dist/MarkerCluster.Default.css";
  import { onMount } from "svelte";

  onMount(async () => {
    const L = (await import("../lib/leafletAndCluster")).leafletAndCluster();

    // Init map
    let ipMap = L.map("ip-map").setView([0.0, 0.0], 0);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(ipMap);

    // Fetch markers and add to map
    // TODO: Make this update every x seconds
    let ipMapMarkers = L.markerClusterGroup();
    const res = await fetch("/data/map");
    const markerList = await res.json();
    markerList.forEach((m) => {
      ipMapMarkers.addLayer(L.marker([m.lat, m.long]));
    });
    ipMap.addLayer(ipMapMarkers);
  });
</script>

<div id="ip-map" class="map"></div>
