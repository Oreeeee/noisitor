<script>
  export let eventList;
  import { formatUnixSecs } from "$lib/dateFormatter";
</script>

<div class="pico">
  <h2>Total events: {eventList.length}</h2>
  <table>
    <tr>
      <th>Time</th>
      <th>Port</th>
    </tr>
    {#each eventList as event}
      <tr>
        <td>{formatUnixSecs(event.time)}</td>
        <td>{event.port}</td>
      </tr>
    {/each}
  </table>
</div>
