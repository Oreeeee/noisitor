// The entire purpose of this module is to merge leaflet and leaflet.markercluster
// so that import() function can be used on it.
// It's fucking stupid, but it works
import "leaflet";
import "leaflet.markercluster";

export function leafletAndCluster() {
  return L;
}
