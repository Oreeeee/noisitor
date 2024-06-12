<script>
  import { onMount } from "svelte";
  import KeepAliveTester from "./KeepAliveTester.svelte";

  let uptime = 0;
  let uptimeHR = "";
  let startedTime = 0;

  onMount(() => {
    fetch("/data/started-time")
      .then((x) => x.text())
      .then((data) => (startedTime = data));

    setInterval(() => {
      const currentTime = Math.round(Date.now() / 1000);
      uptime = currentTime - startedTime;
      const d = Math.floor(uptime / (3600 * 24));
      const h = Math.floor((uptime % (3600 * 24)) / 3600);
      const m = Math.floor((uptime % 3600) / 60);
      const s = Math.floor(uptime % 60);
      uptimeHR = `${d}d:${h}h:${m}m:${s}s`;
    }, 1000);
  });
</script>

<div id="header" class="pico">
  <hgroup>
    <a href="/" style="text-decoration:none">
      <h1 id="name-link">
        <img id="logo" src="/logo.png" alt="Logo">
        Noisitor
      </h1>
    </a>
    <h6>Uptime: {uptimeHR}</h6>
  </hgroup>
  <KeepAliveTester />
</div>
