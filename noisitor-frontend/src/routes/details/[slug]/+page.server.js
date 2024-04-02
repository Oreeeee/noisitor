function validateIPaddress(ipaddress) {
  if (
    /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(
      ipaddress
    )
  ) {
    return true;
  }
  return false;
}

export const load = async ({ params }) => {
  let ip = params.slug;
  let isValid = false;
  let geolocation,
    eventList = undefined;
  if (validateIPaddress(ip)) {
    isValid = true;
    const geolocationRes = fetch(
      `http://backend:8000/data/ip/${ip}/geolocation/`
    );
    const eventListRes = fetch(`http://backend:8000/data/ip/${ip}/event-list/`);
    geolocation = await (await geolocationRes).json();
    eventList = await (await eventListRes).json();
  }
  return {
    ip: params.slug,
    isValid: isValid,
    geolocation: geolocation,
    eventList: eventList,
  };
};
