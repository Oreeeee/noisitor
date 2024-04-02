export function formatUnixSecs(date) {
  const jsDate = new Date(date * 1000);

  const year = singleDigitToZeroPrefix(jsDate.getFullYear());
  const month = singleDigitToZeroPrefix(jsDate.getMonth());
  const day = singleDigitToZeroPrefix(jsDate.getDay());

  const hour = singleDigitToZeroPrefix(jsDate.getHours());
  const minute = singleDigitToZeroPrefix(jsDate.getMinutes());
  const second = singleDigitToZeroPrefix(jsDate.getSeconds());

  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

function singleDigitToZeroPrefix(str) {
  if (str.toString().length == 1) {
    str = "0" + str;
  }
  return str;
}
