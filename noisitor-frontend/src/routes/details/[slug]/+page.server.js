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
  if (validateIPaddress(ip)) {
    isValid = true;
  }
  // TODO: Fetch data here
  return {
    ip: params.slug,
    isValid: isValid,
    geolocation: {},
    eventList: [],
  };
};
