import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../api/client'
import { fieldErrors } from '../utils'

export default function PostForm() {
  const { slug } = useParams()
  const isEdit = Boolean(slug)
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [image, setImage] = useState(null)
  const [preview, setPreview] = useState(null)
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [loading, setLoading] = useState(isEdit)

  useEffect(() => {
    if (!isEdit) return
    api.get(`/posts/${slug}/`)
      .then((r) => {
        setTitle(r.data.title)
        setBody(r.data.body)
        if (r.data.image) setPreview(r.data.image)
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [slug, isEdit, navigate])

  const onImage = (e) => {
    const f = e.target.files?.[0]
    if (!f) return
    setImage(f)
    setPreview(URL.createObjectURL(f))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    setErrors({})
    setSubmitting(true)
    try {
      const fd = new FormData()
      fd.append('title', title)
      fd.append('body', body)
      if (image) fd.append('image', image)
      const cfg = { headers: { 'Content-Type': 'multipart/form-data' } }
      const r = isEdit
        ? await api.patch(`/posts/${slug}/`, fd, cfg)
        : await api.post('/posts/', fd, cfg)
      navigate(`/posts/${r.data.slug}`)
    } catch (err) {
      setErrors(fieldErrors(err) || { _: 'Не удалось сохранить.' })
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="mx-auto max-w-3xl px-4 py-12 text-ink-400">Загружаем…</div>

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="font-serif text-2xl font-semibold text-ink-900">
        {isEdit ? 'Редактировать запись' : 'Новая запись'}
      </h1>
      <p className="mt-1 text-sm text-ink-600">Расскажите что-нибудь полезное.</p>

      <form onSubmit={onSubmit} className="card mt-6 p-6 space-y-4">
        <div>
          <label className="label">Заголовок</label>
          <input
            className="input" value={title} onChange={(e) => setTitle(e.target.value)}
            required maxLength={200} placeholder="О чём пост?"
          />
          {errors.title && <p className="mt-1 text-xs text-red-600">{errors.title}</p>}
        </div>

        <div>
          <label className="label">Текст</label>
          <textarea
            className="input min-h-[240px] font-serif"
            value={body} onChange={(e) => setBody(e.target.value)} required
            placeholder="Пишите как в обычном редакторе. Переносы строк сохранятся."
          />
          {errors.body && <p className="mt-1 text-xs text-red-600">{errors.body}</p>}
        </div>

        <div>
          <label className="label">Обложка <span className="font-normal normal-case text-ink-400">(необязательно)</span></label>
          <input type="file" accept="image/*" onChange={onImage} className="block w-full text-sm" />
          {preview && <img src={preview} alt="" className="mt-3 max-h-56 rounded-xl border border-ink-100" />}
        </div>

        {errors._ && <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{errors._}</div>}

        <div className="flex items-center justify-end gap-2">
          <button type="button" onClick={() => navigate(-1)} className="btn-outline">Отмена</button>
          <button type="submit" disabled={submitting} className="btn-primary">
            {submitting ? 'Сохраняем…' : isEdit ? 'Сохранить' : 'Опубликовать'}
          </button>
        </div>
      </form>
    </div>
  )
}
