<script>
  export let eventData;
  import { twoLetterCodeToFlag } from "$lib/getCountryFlags";
  import { formatUnixSecs } from "$lib/dateFormatter";
</script>

<div class="last-event grid">
  <div>
    <img
      src={twoLetterCodeToFlag(eventData.locationData.country_short)}
      alt="Country flag"
    />
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
    <a href="/details/{eventData.ip}" target="_blank">
      <button class="event-action-button">More info</button>
    </a>
    <a href="https://abuseipdb.com/check/{eventData.ip}" target="_blank"
      ><button class="event-action-button secondary">AbuseIPDB</button></a
    >
  </div>
</div>
