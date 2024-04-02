<script>
  export let data;
  import IpInfo from "../../../components/IPInfo.svelte";
  import PastEvents from "../../../components/PastEvents.svelte";

  const ip = data.ip;
  const eventList = data.eventList;

  var showingScreen = "ipInfo";
  function setScreen(screen) {
    showingScreen = screen;
  }
</script>

<div class="site-contents">
  <center>
    <h1>Viewing info about {ip}</h1>
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
</div>
