import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { fieldErrors } from '../utils'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', email: '', bio: '', password: '', password2: '' })
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  const change = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  const onSubmit = async (e) => {
    e.preventDefault()
    setErrors({})
    setSubmitting(true)
    try {
      await register(form)
      navigate('/', { replace: true })
    } catch (err) {
      setErrors(fieldErrors(err) || { _: 'Не удалось зарегистрироваться.' })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-12">
      <div className="card p-7">
        <h1 className="font-serif text-2xl font-semibold text-ink-900">Создать аккаунт</h1>
        <p className="mt-1 text-sm text-ink-600">Несколько полей — и можно писать.</p>

        <form onSubmit={onSubmit} className="mt-6 space-y-4">
          <div>
            <label className="label">Имя пользователя</label>
            <input className="input" value={form.username} onChange={change('username')} required />
            {errors.username && <p className="mt-1 text-xs text-red-600">{errors.username}</p>}
          </div>
          <div>
            <label className="label">Email</label>
            <input type="email" className="input" value={form.email} onChange={change('email')} required />
            {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email}</p>}
          </div>
          <div>
            <label className="label">О себе <span className="font-normal normal-case text-ink-400">(необязательно)</span></label>
            <textarea className="input min-h-[80px]" value={form.bio} onChange={change('bio')} maxLength={500} />
            {errors.bio && <p className="mt-1 text-xs text-red-600">{errors.bio}</p>}
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="label">Пароль</label>
              <input type="password" className="input" value={form.password} onChange={change('password')} required minLength={6} />
              {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password}</p>}
            </div>
            <div>
              <label className="label">Повторите</label>
              <input type="password" className="input" value={form.password2} onChange={change('password2')} required minLength={6} />
              {errors.password2 && <p className="mt-1 text-xs text-red-600">{errors.password2}</p>}
            </div>
          </div>

          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? 'Создаём…' : 'Создать аккаунт'}
          </button>
        </form>

        <p className="mt-5 text-center text-sm text-ink-600">
          Уже зарегистрированы? <Link to="/login" className="font-medium text-brand-600 hover:underline">Войти</Link>
        </p>
      </div>
    </div>
  )
}
