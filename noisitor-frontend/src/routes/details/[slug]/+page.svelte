<script>
  export let data;
  // TODO: Check did an IP make an event, if not, show an appropiate message
  import IpInfo from "../../../components/IPInfo.svelte";
  import PastEvents from "../../../components/PastEvents.svelte";
  console.log(data.eventList);
  var showingScreen = "ipInfo";
  function setScreen(screen) {
    showingScreen = screen;
  }
</script>

<div class="site-contents">
  {#if !data.isValid}
    <center>
      <h1>{data.ip} is not a valid IP address!</h1>
    </center>
  {:else if JSON.stringify(data.eventList) == "[]"}
    <center>
      <h1>{data.ip} never made any events</h1>
    </center>
  {:else}
    <center>
      <h1>Viewing info about {data.ip}</h1>
    </center>
    <div class="grid pico">
      <button
        on:click={() => {
          setScreen("ipInfo");
        }}>IP info</button
      >
      <button
        on:click={() => {
          setScreen("pastEvents");
        }}>Past events</button
      >
    </div>
    <br />
    {#if showingScreen == "ipInfo"}
      <IpInfo ip />
    {:else if showingScreen == "pastEvents"}
      <PastEvents eventList />
    {/if}
  {/if}
</div>
