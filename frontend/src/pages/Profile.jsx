import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'
import { Avatar } from '../components/Navbar'
import { timeAgo, fieldErrors } from '../utils'

export default function Profile() {
  const { user, setUser, refreshUser, logout } = useAuth()
  const [myPosts, setMyPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ username: '', bio: '' })
  const [avatarFile, setAvatarFile] = useState(null)
  const [avatarPreview, setAvatarPreview] = useState(null)
  const [errors, setErrors] = useState({})
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!user) return
    setForm({ username: user.username, bio: user.bio || '' })
    api.get('/posts/', { params: { author: user.id } })
      .then((r) => setMyPosts(r.data.results))
      .catch(() => setMyPosts([]))
      .finally(() => setLoading(false))
  }, [user])

  const onPickAvatar = (e) => {
    const f = e.target.files?.[0]
    if (!f) return
    setAvatarFile(f)
    setAvatarPreview(URL.createObjectURL(f))
  }

  const onSave = async (e) => {
    e.preventDefault()
    setErrors({})
    setSaving(true)
    try {
      const fd = new FormData()
      fd.append('username', form.username)
      fd.append('bio', form.bio)
      if (avatarFile) fd.append('avatar', avatarFile)
      const r = await api.patch('/auth/me/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      setUser(r.data)
      setEditing(false)
      setAvatarFile(null)
      setAvatarPreview(null)
    } catch (err) {
      setErrors(fieldErrors(err) || { _: 'Не удалось сохранить.' })
    } finally {
      setSaving(false)
    }
  }

  if (!user) return null

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <div className="card p-6 sm:p-8">
        <div className="flex flex-col items-start gap-6 sm:flex-row sm:items-center">
          <div className="relative">
            <Avatar user={user} size="lg" />
            {editing && (
              <label className="absolute inset-0 grid cursor-pointer place-items-center rounded-full bg-black/40 text-xs font-medium text-white opacity-0 hover:opacity-100 transition">
                Сменить
                <input type="file" accept="image/*" onChange={onPickAvatar} className="hidden" />
              </label>
            )}
          </div>
          <div className="flex-1">
            <h1 className="font-serif text-2xl font-semibold text-ink-900">{user.username}</h1>
            <p className="text-sm text-ink-600">{user.email}</p>
            <p className="mt-2 max-w-xl text-sm text-ink-900">
              {user.bio || <span className="italic text-ink-400">Расскажите о себе в настройках профиля.</span>}
            </p>
            <div className="mt-3 flex gap-2 text-xs text-ink-600">
              <span className="badge">{user.posts_count} постов</span>
              <span className="badge">{user.comments_count} комментариев</span>
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <button onClick={() => setEditing((v) => !v)} className="btn-outline">
              {editing ? 'Отменить' : 'Редактировать профиль'}
            </button>
            <button onClick={logout} className="btn-ghost text-red-600">Выйти</button>
          </div>
        </div>

        {editing && (
          <form onSubmit={onSave} className="mt-6 border-t border-ink-100 pt-6 space-y-4">
            {avatarPreview && <img src={avatarPreview} alt="" className="h-20 w-20 rounded-full object-cover" />}
            <div>
              <label className="label">Имя пользователя</label>
              <input className="input" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} required />
              {errors.username && <p className="mt-1 text-xs text-red-600">{errors.username}</p>}
            </div>
            <div>
              <label className="label">О себе</label>
              <textarea className="input min-h-[100px]" value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} maxLength={500} />
              {errors.bio && <p className="mt-1 text-xs text-red-600">{errors.bio}</p>}
            </div>
            {errors._ && <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{errors._}</div>}
            <button disabled={saving} className="btn-primary">
              {saving ? 'Сохраняем…' : 'Сохранить'}
            </button>
          </form>
        )}
      </div>

      <h2 className="mt-10 mb-4 text-lg font-semibold text-ink-900">Мои записи</h2>
      {loading && <div className="text-ink-400">Загружаем…</div>}
      {!loading && myPosts.length === 0 && (
        <div className="card p-8 text-center text-ink-600">
          У вас пока нет постов. <Link to="/posts/new" className="text-brand-600 hover:underline">Написать первый.</Link>
        </div>
      )}
      <div className="grid gap-3">
        {myPosts.map((p) => (
          <Link to={`/posts/${p.slug}`} key={p.id} className="card flex items-center justify-between p-4 hover:border-ink-200">
            <div>
              <h3 className="font-semibold text-ink-900">{p.title}</h3>
              <p className="mt-1 text-xs text-ink-600">
                {timeAgo(p.created_at)} · 💬 {p.comments_count}
              </p>
            </div>
            <span className="text-ink-400">→</span>
          </Link>
        ))}
      </div>
    </div>
  )
}
