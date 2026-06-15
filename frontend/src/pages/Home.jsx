import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'
import { timeAgo } from '../utils'
import { Avatar } from '../components/Navbar'

export default function Home() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')

  useEffect(() => {
    let cancel = false
    setLoading(true)
    api.get('/posts/', { params: { search: query || undefined } })
      .then((r) => { if (!cancel) setPosts(r.data.results) })
      .catch(() => { if (!cancel) setError('Не удалось загрузить посты.') })
      .finally(() => { if (!cancel) setLoading(false) })
    return () => { cancel = true }
  }, [query])

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <section className="rounded-3xl bg-gradient-to-br from-brand-600 to-ink-900 px-6 py-10 text-white sm:px-10 sm:py-14">
        <h1 className="font-serif text-3xl font-semibold sm:text-4xl">
          Заметки о коде, дизайне и ремесле
        </h1>
        <p className="mt-2 max-w-xl text-white/80">
          Маленький блог, где разработчики делятся опытом и обсуждают идеи в комментариях.
        </p>
        <div className="mt-6 flex max-w-md gap-2 rounded-2xl bg-white/10 p-1.5 backdrop-blur">
          <input
            value={query} onChange={(e) => setQuery(e.target.value)}
            placeholder="Поиск по заголовку и тексту…"
            className="flex-1 rounded-xl bg-transparent px-3 py-2 text-sm placeholder:text-white/50 focus:outline-none"
          />
          <button onClick={() => setQuery(query)} className="rounded-xl bg-white px-3 py-2 text-sm font-semibold text-ink-900 hover:bg-ink-50">
            Найти
          </button>
        </div>
      </section>

      <h2 className="mt-10 mb-4 text-lg font-semibold text-ink-900">Свежие записи</h2>

      {loading && <div className="text-ink-400">Загружаем…</div>}
      {error && <div className="rounded-lg bg-red-50 p-4 text-red-700">{error}</div>}
      {!loading && !error && posts.length === 0 && (
        <div className="card p-8 text-center text-ink-600">
          Пока нет постов по запросу. <Link to="/posts/new" className="text-brand-600 hover:underline">Напишите первый.</Link>
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        {posts.map((p) => (
          <Link to={`/posts/${p.slug}`} key={p.id} className="card p-5 group block">
            <div className="flex items-center gap-2 text-xs text-ink-600">
              <Avatar user={p.author} size="sm" />
              <span className="font-medium text-ink-900">{p.author.username}</span>
              <span>·</span>
              <span>{timeAgo(p.created_at)}</span>
            </div>
            <h3 className="mt-3 font-serif text-xl font-semibold text-ink-900 group-hover:text-brand-700">
              {p.title}
            </h3>
            <p className="mt-2 line-clamp-3 text-sm text-ink-600">{p.excerpt}</p>
            <div className="mt-4 flex items-center gap-3 text-xs text-ink-600">
              <span className="badge">💬 {p.comments_count} комм.</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
