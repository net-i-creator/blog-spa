import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="mx-auto max-w-md px-4 py-20 text-center">
      <div className="font-serif text-7xl text-ink-200">404</div>
      <h1 className="mt-4 font-serif text-2xl font-semibold">Страница не найдена</h1>
      <p className="mt-2 text-ink-600">Возможно, ссылка устарела или была удалена.</p>
      <Link to="/" className="btn-primary mt-6 inline-flex">На главную</Link>
    </div>
  )
}
