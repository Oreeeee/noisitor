import "./style.css";
import "@picocss/pico/css/pico.conditional.min.css";
import "htmx.org";
import "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.markercluster";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";

var ipMap = L.map("ip-map").setView([0, 0], 0);
var ipMapMarkers = L.markerClusterGroup();

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(ipMap);

fetch("/data/map")
  .then((response) => response.text())
  .then((text) => {
    const responseArr = text.split("\n");
    responseArr.forEach((element) => {
      try {
        ipMapMarkers.addLayer(L.marker(element.split("|")));
      } catch (e) {
        console.log(e);
      }
    });
  });

ipMap.addLayer(ipMapMarkers);
