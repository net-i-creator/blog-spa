import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { fieldErrors } from '../utils'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    setErrors({})
    setSubmitting(true)
    try {
      await login(email, password)
      const to = location.state?.from?.pathname || '/'
      navigate(to, { replace: true })
    } catch (err) {
      setErrors(fieldErrors(err) || { _: 'Не удалось войти.' })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-12">
      <div className="card p-7">
        <h1 className="font-serif text-2xl font-semibold text-ink-900">С возвращением</h1>
        <p className="mt-1 text-sm text-ink-600">Войдите, чтобы писать посты и оставлять комментарии.</p>

        <form onSubmit={onSubmit} className="mt-6 space-y-4">
          <div>
            <label className="label">Email</label>
            <input
              type="email" className="input" value={email}
              onChange={(e) => setEmail(e.target.value)} required autoFocus
              placeholder="you@example.com"
            />
            {errors.email && <FieldError text={errors.email} />}
          </div>
          <div>
            <label className="label">Пароль</label>
            <input
              type="password" className="input" value={password}
              onChange={(e) => setPassword(e.target.value)} required
              placeholder="••••••••"
            />
            {errors.password && <FieldError text={errors.password} />}
          </div>
          {errors._ && <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{errors._}</div>}

          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? 'Входим…' : 'Войти'}
          </button>
        </form>

        <p className="mt-5 text-center text-sm text-ink-600">
          Нет аккаунта? <Link to="/register" className="font-medium text-brand-600 hover:underline">Зарегистрироваться</Link>
        </p>
        <div className="mt-4 rounded-lg bg-ink-50 p-3 text-xs text-ink-600">
          <b>Демо:</b> alice@example.com / password123
        </div>
      </div>
    </div>
  )
}

function FieldError({ text }) {
  return <p className="mt-1 text-xs text-red-600">{text}</p>
}
