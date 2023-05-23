import axios from 'axios'
import apiURL from './config'

const api = axios.create({
  baseURL: apiURL,
  headers: {},
})

export default api