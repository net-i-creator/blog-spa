import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useState } from 'react'
import { initials } from '../utils'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  const linkClass = ({ isActive }) =>
    `px-3 py-2 rounded-lg text-sm font-medium transition ${
      isActive ? 'text-brand-700 bg-brand-50' : 'text-ink-600 hover:text-ink-900 hover:bg-ink-100'
    }`

  return (
    <header className="sticky top-0 z-30 border-b border-ink-100 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2 font-serif text-lg font-semibold text-ink-900">
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-white">Б</span>
          Блог<span className="text-ink-400">.</span>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          <NavLink to="/" end className={linkClass}>Лента</NavLink>
          {user && <NavLink to="/posts/new" className={linkClass}>Новая запись</NavLink>}
          {user && <NavLink to="/profile" className={linkClass}>Кабинет</NavLink>}
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          {user ? (
            <>
              <Link to={`/users/${user.id}`} className="flex items-center gap-2 rounded-full p-1 pr-3 hover:bg-ink-100">
                <Avatar user={user} size="sm" />
                <span className="text-sm font-medium">{user.username}</span>
              </Link>
              <button
                onClick={() => { logout(); navigate('/') }}
                className="btn-ghost"
              >Выйти</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-ghost">Войти</Link>
              <Link to="/register" className="btn-primary">Регистрация</Link>
            </>
          )}
        </div>

        <button
          onClick={() => setOpen((v) => !v)}
          className="md:hidden btn-ghost !p-2"
          aria-label="Меню"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 6h18M3 12h18M3 18h18" strokeLinecap="round" />
          </svg>
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-ink-100 bg-white">
          <div className="mx-auto max-w-6xl flex flex-col gap-1 px-4 py-3">
            <NavLink to="/" end className={linkClass} onClick={() => setOpen(false)}>Лента</NavLink>
            {user && <NavLink to="/posts/new" className={linkClass} onClick={() => setOpen(false)}>Новая запись</NavLink>}
            {user && <NavLink to="/profile" className={linkClass} onClick={() => setOpen(false)}>Кабинет</NavLink>}
            {user ? (
              <button
                onClick={() => { setOpen(false); logout(); navigate('/') }}
                className="btn-outline mt-2"
              >Выйти из {user.username}</button>
            ) : (
              <div className="flex gap-2 mt-2">
                <Link to="/login" onClick={() => setOpen(false)} className="btn-outline flex-1">Войти</Link>
                <Link to="/register" onClick={() => setOpen(false)} className="btn-primary flex-1">Регистрация</Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  )
}

export function Avatar({ user, size = 'md' }) {
  const sizes = { sm: 'h-7 w-7 text-xs', md: 'h-9 w-9 text-sm', lg: 'h-16 w-16 text-lg' }
  const sz = sizes[size] || sizes.md
  return (
    <div className={`grid place-items-center overflow-hidden rounded-full bg-gradient-to-br from-brand-100 to-brand-500 font-semibold text-white ${sz}`}>
      {user?.avatar ? (
        <img src={user.avatar} alt={user.username} className="h-full w-full object-cover" />
      ) : (
        <span>{initials(user?.username)}</span>
      )}
    </div>
  )
}
