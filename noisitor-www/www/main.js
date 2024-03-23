import "./style.css";
import "@picocss/pico/css/pico.conditional.min.css";
import "htmx.org";
import "leaflet";
import "leaflet/dist/leaflet.css";

var ipMap = L.map("ip-map").setView([0, 0], 0);
//var gjLayer = L.geoJSON().addTo(ipMap);

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
        L.marker(element.split("|")).addTo(ipMap);
      } catch (e) {
        console.log(e);
      }
    });
  });
