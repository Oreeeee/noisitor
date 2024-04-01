import { fetchUniqueIPs, fetchEventsLogged, fetchLastEvents } from "../lib/fetchStats.js";

export const load = async () => {
  return {
    uniqueIPs: await fetchUniqueIPs(true),
    eventsLogged: await fetchEventsLogged(true),
    lastEvents: await fetchLastEvents(true),
  };
};
