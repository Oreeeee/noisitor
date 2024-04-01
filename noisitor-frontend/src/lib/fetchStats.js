// TODO: Make this fetching better, maybe fetch one JSON file?
export async function fetchUniqueIPs() {
  const res = await fetch("/data/unique-ips");
  const ret = await res.text();
  return ret;
}

export async function fetchEventsLogged() {
  const res = await fetch("/data/total-events");
  const ret = await res.text();
  return ret;
}
