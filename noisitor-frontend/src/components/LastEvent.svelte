<script>
  export let eventData;
  import { twoLetterCodeToFlag } from "$lib/getCountryFlags";
  import { formatUnixSecs } from "$lib/dateFormatter";
  import MoreInfoButton from "./MoreInfoButton.svelte";
  import AbuseIpdbButton from "./AbuseIPDBButton.svelte";
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
    <MoreInfoButton ip={eventData.ip} wide={true} /><br><br>
    <AbuseIpdbButton ip={eventData.ip} wide={true} />
  </div>
</div>
