import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import PostDetail from './pages/PostDetail'
import PostForm from './pages/PostForm'
import Profile from './pages/Profile'
import UserPage from './pages/UserPage'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/posts/:slug" element={<PostDetail />} />
              <Route path="/users/:id" element={<UserPage />} />
              <Route
                path="/posts/new"
                element={<ProtectedRoute><PostForm /></ProtectedRoute>}
              />
              <Route
                path="/posts/:slug/edit"
                element={<ProtectedRoute><PostForm /></ProtectedRoute>}
              />
              <Route
                path="/profile"
                element={<ProtectedRoute><Profile /></ProtectedRoute>}
              />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <footer className="border-t border-ink-100 py-6 text-center text-xs text-ink-400">
            Учебный проект · Django REST Framework + React + Tailwind
          </footer>
        </div>
      </BrowserRouter>
    </AuthProvider>
  )
}
