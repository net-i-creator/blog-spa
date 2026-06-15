import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

let accessToken = null
let onUnauthorized = null

export function setAccessToken(token) {
  accessToken = token
}
export function getAccessToken() {
  return accessToken
}
export function setUnauthorizedHandler(fn) {
  onUnauthorized = fn
}

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (
      error.response?.status === 401 &&
      !original._retry &&
      !original.url?.endsWith('/auth/login/') &&
      !original.url?.endsWith('/auth/token/refresh/') &&
      localStorage.getItem('refresh')
    ) {
      original._retry = true
      try {
        const r = await axios.post('/api/auth/token/refresh/', {
          refresh: localStorage.getItem('refresh'),
        })
        const newAccess = r.data.access
        setAccessToken(newAccess)
        localStorage.setItem('access', newAccess)
        original.headers.Authorization = `Bearer ${newAccess}`
        return api(original)
      } catch {
        if (onUnauthorized) onUnauthorized()
      }
    }
    return Promise.reject(error)
  }
)

export default api
