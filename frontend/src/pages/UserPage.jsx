import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import api from '../api/client'
import { timeAgo } from '../utils'
import { Avatar } from '../components/Navbar'

export default function UserPage() {
  const { id } = useParams()
  const [profile, setProfile] = useState(null)
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      api.get(`/auth/users/${id}/`),
      api.get('/posts/', { params: { author: id } }),
    ])
      .then(([u, p]) => { setProfile(u.data); setPosts(p.data.results) })
      .catch(() => setError('Пользователь не найден.'))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="mx-auto max-w-4xl px-4 py-12 text-ink-400">Загружаем…</div>
  if (error || !profile) return <div className="mx-auto max-w-4xl px-4 py-12 text-red-700">{error || 'Ошибка'}</div>

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <div className="card p-6 sm:p-8">
        <div className="flex flex-col items-start gap-6 sm:flex-row sm:items-center">
          <Avatar user={profile} size="lg" />
          <div className="flex-1">
            <h1 className="font-serif text-2xl font-semibold text-ink-900">{profile.username}</h1>
            <p className="text-sm text-ink-600">На сайте с {new Date(profile.date_joined).toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })}</p>
            {profile.bio && <p className="mt-3 max-w-xl text-sm text-ink-900">{profile.bio}</p>}
            <div className="mt-3 flex gap-2 text-xs text-ink-600">
              <span className="badge">{profile.posts_count} постов</span>
              <span className="badge">{profile.comments_count} комментариев</span>
            </div>
          </div>
        </div>
      </div>

      <h2 className="mt-10 mb-4 text-lg font-semibold text-ink-900">Записи автора</h2>
      {posts.length === 0 && <div className="text-ink-400">Пока нет записей.</div>}
      <div className="grid gap-3">
        {posts.map((p) => (
          <Link to={`/posts/${p.slug}`} key={p.id} className="card p-4">
            <h3 className="font-semibold text-ink-900">{p.title}</h3>
            <p className="mt-1 line-clamp-2 text-sm text-ink-600">{p.excerpt}</p>
            <p className="mt-2 text-xs text-ink-400">{timeAgo(p.created_at)} · 💬 {p.comments_count}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
