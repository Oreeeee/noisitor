export function twoLetterCodeToFlag(code = "-") {
  if (code == "-") {
    return "";
  }
  return `https://catamphetamine.gitlab.io/country-flag-icons/3x2/${code}.svg`;
}
