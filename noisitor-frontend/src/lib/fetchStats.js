// TODO: Make this fetching better, maybe fetch one JSON file?
export async function fetchStats(server = false) {
  let endpoint;
  if (server) {
    endpoint = "http://backend:8000/data/stats.json";
  } else {
    endpoint = "/data/stats.json";
  }
  const res = await fetch(endpoint);
  const ret = await res.json();
  return ret;
}

export async function fetchEvents(server = false, count) {
  let endpoint;
  if (server) {
    endpoint = `http://backend:8000/data/events/${count}`;
  } else {
    endpoint = `/data/events/${count}`;
  }
  const res = await fetch(endpoint);
  const ret = await res.json();
  return ret;
}
