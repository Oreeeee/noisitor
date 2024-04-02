export const load = async ({ params }) => {
  // TODO: Verify is IP in slug valid, otherwise return error
  // TODO: Fetch data here
  return {
    ip: params.slug,
    geolocation: {},
    eventList: [],
  };
};
