export function timeAgo(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const diff = (Date.now() - d.getTime()) / 1000
  if (diff < 60) return 'только что'
  if (diff < 3600) return `${Math.floor(diff / 60)} мин назад`
  if (diff < 86400) return `${Math.floor(diff / 3600)} ч назад`
  if (diff < 86400 * 7) return `${Math.floor(diff / 86400)} дн назад`
  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
}

export function fullDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}

export function avatarUrl(user) {
  if (!user?.avatar) return null
  if (user.avatar.startsWith('http')) return user.avatar
  return user.avatar
}

export function initials(name) {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  return (parts[0]?.[0] || '') + (parts[1]?.[0] || '')
}

export function fieldErrors(error) {
  const data = error?.response?.data
  if (!data) return null
  if (typeof data === 'string') return { _: data }
  if (data.detail) return { _: data.detail }
  const out = {}
  for (const [k, v] of Object.entries(data)) {
    out[k] = Array.isArray(v) ? v.join(' ') : String(v)
  }
  return out
}
