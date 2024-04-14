<script>
  export let data;
  import MoreInfoButton from "../../components/MoreInfoButton.svelte";
  import { formatUnixSecs } from "$lib/dateFormatter";
  import { fetchEvents } from "$lib/fetchStats";

  const getAtOnce = 100;
  let events = data.events;
  let count = getAtOnce * 2;
  let canFetchMore = true;

  async function fetchMoreEvents() {
    const newEvents = await fetchEvents(false, count);
    events = newEvents;
    if (newEvents.length < getAtOnce) {
      canFetchMore = false;
    }
    count += getAtOnce;
  }
</script>

<div class="site-contents pico">
  <table>
    <tr>
      <th><strong>IP</strong></th>
      <th><strong>Port</strong></th>
      <th><strong>Time</strong></th>
      <th><strong>More info</strong></th>
    </tr>
    {#each events as event}
      <tr>
        <td>{event.ip}</td>
        <td>{event.port}</td>
        <td>{formatUnixSecs(event.dt)}</td>
        <td><MoreInfoButton ip={event.ip} /></td>
      </tr>
    {/each}
  </table>
  {#if canFetchMore}
    <button class="wide-button" on:click={fetchMoreEvents}>Fetch more</button>
  {/if}
</div>
