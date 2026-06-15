import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'
import { timeAgo, fullDate, fieldErrors } from '../utils'
import { Avatar } from '../components/Navbar'

export default function PostDetail() {
  const { slug } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [text, setText] = useState('')
  const [posting, setPosting] = useState(false)
  const [postError, setPostError] = useState(null)

  const load = () => {
    setLoading(true)
    api.get(`/posts/${slug}/`)
      .then((r) => setPost(r.data))
      .catch(() => setError('Пост не найден.'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [slug])

  const onAddComment = async (e) => {
    e.preventDefault()
    if (!text.trim()) return
    setPostError(null)
    setPosting(true)
    try {
      const r = await api.post(`/posts/${slug}/comments/`, { text })
      setPost((p) => ({ ...p, comments: [...p.comments, r.data] }))
      setText('')
    } catch (err) {
      setPostError(fieldErrors(err) || { _: 'Не удалось отправить комментарий.' })
    } finally {
      setPosting(false)
    }
  }

  const onDeleteComment = async (id) => {
    if (!confirm('Удалить комментарий?')) return
    try {
      await api.delete(`/comments/${id}/`)
      setPost((p) => ({ ...p, comments: p.comments.filter((c) => c.id !== id) }))
    } catch {
      alert('Не удалось удалить комментарий.')
    }
  }

  const onDeletePost = async () => {
    if (!confirm('Удалить пост? Действие необратимо.')) return
    try {
      await api.delete(`/posts/${slug}/`)
      navigate('/')
    } catch {
      alert('Не удалось удалить пост.')
    }
  }

  if (loading) return <div className="mx-auto max-w-3xl px-4 py-12 text-ink-400">Загружаем…</div>
  if (error || !post) return <div className="mx-auto max-w-3xl px-4 py-12 text-red-700">{error || 'Ошибка'}</div>

  const isAuthor = user && post.author.id === user.id

  return (
    <article className="mx-auto max-w-3xl px-4 py-8">
      <Link to="/" className="text-sm text-ink-600 hover:text-ink-900">← Назад к ленте</Link>

      <header className="mt-4">
        <h1 className="font-serif text-3xl font-semibold text-ink-900 sm:text-4xl">{post.title}</h1>
        <div className="mt-4 flex items-center justify-between">
          <Link to={`/users/${post.author.id}`} className="flex items-center gap-2 text-sm text-ink-600 hover:text-ink-900">
            <Avatar user={post.author} size="sm" />
            <span className="font-medium text-ink-900">{post.author.username}</span>
            <span>·</span>
            <span>{fullDate(post.created_at)}</span>
          </Link>
          {isAuthor && (
            <div className="flex gap-2">
              <Link to={`/posts/${post.slug}/edit`} className="btn-outline">Редактировать</Link>
              <button onClick={onDeletePost} className="btn-outline text-red-600 hover:bg-red-50">Удалить</button>
            </div>
          )}
        </div>
      </header>

      {post.image && <img src={post.image} alt="" className="mt-6 w-full rounded-2xl" />}

      <div className="prose-article mt-8 whitespace-pre-line text-ink-900">{post.body}</div>

      <hr className="my-10 border-ink-100" />

      <section>
        <h2 className="font-serif text-xl font-semibold text-ink-900">Комментарии ({post.comments.length})</h2>

        {user ? (
          <form onSubmit={onAddComment} className="mt-4">
            <textarea
              className="input min-h-[88px]"
              placeholder="Что думаете?"
              value={text} onChange={(e) => setText(e.target.value)}
              maxLength={1000}
            />
            {postError?._ && <p className="mt-1 text-xs text-red-600">{postError._}</p>}
            {postError?.text && <p className="mt-1 text-xs text-red-600">{postError.text}</p>}
            <div className="mt-2 flex items-center justify-between">
              <span className="text-xs text-ink-400">{text.length}/1000</span>
              <button disabled={posting || !text.trim()} className="btn-primary">
                {posting ? 'Отправляем…' : 'Отправить'}
              </button>
            </div>
          </form>
        ) : (
          <div className="mt-4 rounded-xl border border-dashed border-ink-200 p-4 text-sm text-ink-600">
            <Link to="/login" className="text-brand-600 hover:underline">Войдите</Link>, чтобы оставить комментарий.
          </div>
        )}

        <ul className="mt-6 space-y-3">
          {post.comments.length === 0 && (
            <li className="text-sm text-ink-400">Пока никто не комментировал — будьте первым.</li>
          )}
          {post.comments.map((c) => (
            <li key={c.id} className="card p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-sm">
                  <Avatar user={c.author} size="sm" />
                  <Link to={`/users/${c.author.id}`} className="font-medium text-ink-900 hover:underline">
                    {c.author.username}
                  </Link>
                  <span className="text-ink-400">· {timeAgo(c.created_at)}</span>
                </div>
                {user && c.author.id === user.id && (
                  <button onClick={() => onDeleteComment(c.id)} className="text-xs text-ink-400 hover:text-red-600">
                    удалить
                  </button>
                )}
              </div>
              <p className="mt-2 whitespace-pre-line text-sm text-ink-900">{c.text}</p>
            </li>
          ))}
        </ul>
      </section>
    </article>
  )
}
