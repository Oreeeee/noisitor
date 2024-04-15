import { fetchStartedTime, fetchMonitoredPorts } from "../../lib/fetchStats";

export const load = async () => {
  return {
    runningSince: await fetchStartedTime(),
    monitoredPorts: await fetchMonitoredPorts(),
  };
};
