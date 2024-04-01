// TODO: Make this fetching better, maybe fetch one JSON file?
export async function fetchUniqueIPs(server = false) {
  let endpoint;
  if (server) {
    endpoint = "http://backend:8000/data/unique-ips";
  } else {
    endpoint = "/data/unique-ips";
  }
  const res = await fetch(endpoint);
  const ret = await res.text();
  return ret;
}

export async function fetchEventsLogged(server = false) {
  let endpoint;
  if (server) {
    endpoint = "http://backend:8000/data/total-events";
  } else {
    endpoint = "/data/total-events";
  }
  const res = await fetch(endpoint);
  const ret = await res.text();
  return ret;
}
