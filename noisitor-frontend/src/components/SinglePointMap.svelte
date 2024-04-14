<script>
  export let lat;
  export let long;

  const coords = [parseFloat(lat), parseFloat(long)];

  import "leaflet/dist/leaflet.css";
  import markerIconUrl from "leaflet/dist/images/marker-icon.png";
  import markerIconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
  import markerShadowUrl from "leaflet/dist/images/marker-shadow.png";
  import { onMount } from "svelte";

  onMount(async () => {
    const L = await import("leaflet");

    let spMap = L.map("single-point-map").setView(coords, 13);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(spMap);

    L.Icon.Default.prototype.options.iconUrl = markerIconUrl;
    L.Icon.Default.prototype.options.iconRetinaUrl = markerIconRetinaUrl;
    L.Icon.Default.prototype.options.shadowUrl = markerShadowUrl;
    L.Icon.Default.imagePath = "";

    L.marker(coords).addTo(spMap);
  });
</script>

<div id="single-point-map" class="map"></div>
