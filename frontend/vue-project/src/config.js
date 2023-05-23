const URL_DEV = `http://127.0.0.1:8000`

function getURL(){
  if (import.meta.env.VUE_APP_MODE === "prod") {
    return `${window.location.protocol}//${window.location.hostname}:8765`
  } else {
    return URL_DEV
  }
}

const apiURL = getURL()
console.log(apiURL)
export default apiURL