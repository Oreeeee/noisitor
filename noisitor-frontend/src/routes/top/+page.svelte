<script>
  export let data;
  let tops = data.tops;

  let showingScreen = "ip";
  function setScreen(screen) {
    showingScreen = screen;
  }
</script>

<div class="site-contents pico">
  <div class="grid">
    <button
      on:click={() => {
        setScreen("ip");
      }}>Top IPs</button
    >
    <button
      on:click={() => {
        setScreen("country");
      }}>Top countries</button
    >
    <button
      on:click={() => {
        setScreen("port");
      }}>Top ports</button
    >
  </div>

  <br />

  {#if showingScreen == "ip"}
    <div>
      <h3>Top IP addresses</h3>
      <hr />
      <table>
        <tr>
          <th><strong>IP</strong></th>
          <th><strong>Count</strong></th>
        </tr>
        {#each tops.ips as ip}
          <tr>
            <td>{ip.ip}</td>
            <td>{ip.count}</td>
          </tr>
        {/each}
      </table>
    </div>
  {:else if (showingScreen == "country")}
    <div>
      <h3>Top countries</h3>
      <hr />
      <table>
        <tr>
          <th><strong>Country</strong></th>
          <th><strong>Count</strong></th>
        </tr>
        {#each tops.countries as country}
          <tr>
            <td>{country.country_long}</td>
            <td>{country.count}</td>
          </tr>
        {/each}
      </table>
    </div>
  {:else if (showingScreen == "port")}
    <div>
      <h3>Top ports</h3>
      <hr />
      <table>
        <tr>
          <th><strong>Port</strong></th>
          <th><strong>Count</strong></th>
        </tr>
        {#each tops.ports as port}
          <tr>
            <td>{port.port}</td>
            <td>{port.count}</td>
          </tr>
        {/each}
      </table>
    </div>
  {/if}
</div>
