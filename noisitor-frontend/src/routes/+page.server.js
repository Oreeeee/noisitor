import { fetchStats } from "../lib/fetchStats.js";

export const load = async () => {
  return {
    stats: await fetchStats(true),
  };
};
