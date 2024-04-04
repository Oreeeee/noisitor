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

export async function fetchLastEvents(server = false) {
  let endpoint;
  if (server) {
    endpoint = "http://backend:8000/data/last-events";
  } else {
    endpoint = "/data/last-events";
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
