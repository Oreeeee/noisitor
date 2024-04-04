import { fetchEvents } from "../../lib/fetchStats";

export const load = async () => {
  return {
    events: await fetchEvents(true, 100),
  };
};
