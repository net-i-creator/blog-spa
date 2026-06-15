import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import api, { setAccessToken, setUnauthorizedHandler } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const logout = useCallback(() => {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    setAccessToken(null)
    setUser(null)
  }, [])

  useEffect(() => {
    setUnauthorizedHandler(() => logout())
    const access = localStorage.getItem('access')
    const refresh = localStorage.getItem('refresh')
    if (access && refresh) {
      setAccessToken(access)
      api.get('/auth/me/')
        .then((r) => setUser(r.data))
        .catch(() => logout())
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [logout])

  const login = async (email, password) => {
    const r = await api.post('/auth/login/', { email, password })
    const { access, refresh, user: u } = r.data
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    setAccessToken(access)
    setUser(u)
    return u
  }

  const register = async (payload) => {
    const r = await api.post('/auth/register/', payload)
    const { access, refresh, user: u } = r.data
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    setAccessToken(access)
    setUser(u)
    return u
  }

  const refreshUser = async () => {
    const r = await api.get('/auth/me/')
    setUser(r.data)
    return r.data
  }

  return (
    <AuthContext.Provider value={{ user, setUser, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
