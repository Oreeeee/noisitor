import "./style.css";
import "@picocss/pico/css/pico.conditional.min.css";
import "htmx.org";
import "leaflet"
import "leaflet/dist/leaflet.css"

var ipMap = L.map("ip-map").setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(ipMap);
