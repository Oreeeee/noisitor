import { fetchTops } from "../../lib/fetchStats";

export const load = async () => {
  return {
    tops: await fetchTops(),
  };
};
