<script>
  var uptime = 0;
  var startedTime = 1711849267;

  // TODO: fix fetching errors when building
  //   fetch("/data/started-time")
  //     .then((x) => x.text())
  //     .then((data) => (startedTime = data));

  setInterval(() => {
    const currentTime = Math.round(Date.now() / 1000);
    uptime = currentTime - startedTime;
  }, 1000);
</script>

<div id="header" class="pico">
  <h1>Noisitor</h1>
  <h6>Uptime: {uptime}</h6>
</div>
