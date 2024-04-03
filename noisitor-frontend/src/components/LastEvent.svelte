<script>
  export let eventData;
  import { twoLetterCodeToFlag } from "$lib/getCountryFlags";
  import { formatUnixSecs } from "$lib/dateFormatter";
</script>

<div class="last-event grid">
  <div>
    {#if !(eventData.locationData.country_long == "-" && eventData.locationData.country_short == "-")}
      <img
        src={twoLetterCodeToFlag(eventData.locationData.country_short)}
        alt="{eventData.locationData.country_long} flag"
      />
    {:else}
      <img src="/unknown_flag.svg" alt="Unknown country flag" />
    {/if}
  </div>
  <div>
    <hgroup>
      <h5>{eventData.ip}</h5>
      <p>{eventData.locationData.country_long}</p>
      <p>Port: {eventData.port}</p>
      <p>Time: {formatUnixSecs(eventData.time)}</p>
    </hgroup>
  </div>
  <div>
    <a href="/details/{eventData.ip}">
      <button class="wide-button">More info</button>
    </a><br /><br />
    <a href="https://abuseipdb.com/check/{eventData.ip}" target="_blank"
      ><button class="wide-button secondary">AbuseIPDB</button></a
    >
  </div>
</div>
