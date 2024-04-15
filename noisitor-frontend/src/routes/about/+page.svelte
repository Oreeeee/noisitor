<script>
  export let data;
  const runningSince = data.runningSince;
  const monitoredPorts = data.monitoredPorts;
  import { formatUnixSecs } from "$lib/dateFormatter";
</script>

<div class="site-contents">
  <center>
    <p>Server started on: {formatUnixSecs(runningSince)}</p>
    <p>Monitoring on ports: {monitoredPorts.join(", ")}</p>
    <p>Noisitor uses the IP2Location LITE database for <a href="https://lite.ip2location.com">IP geolocation</a>.</p>
    <p>
      Source code: <a href="https://github.com/Oreeeee/noisitor" target="_blank"
        >https://github.com/Oreeeee/noisitor</a
      >
    </p>
  </center>
</div>
