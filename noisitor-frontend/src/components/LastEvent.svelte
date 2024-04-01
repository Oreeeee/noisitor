<script>
  export let eventData;
  import { twoLetterCodeToFlag } from "$lib/getCountryFlags";
</script>

<div class="last-event grid">
  <div>
    <img
      src={twoLetterCodeToFlag(eventData.locationData.country_short)}
      alt="Country flag"
    />
  </div>
  <div>
    <h3>{eventData.ip}</h3>
    <h5>Country: {eventData.locationData.country_long}</h5>
    <p>Port: {eventData.port}</p>
    <p>Time: {eventData.time}</p>
  </div>
</div>
