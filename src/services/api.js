import axios from "axios"

export default axios.create({
  baseURL: "http://localhost:8000/api",
  //baseURL: "https://13-air-ajtd.rxq.ch/api",
  timeout: 5000,
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN",
  withXSRFToken: true,
  headers: {
    "Content-Type": "application/json"
  }
})
