import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Navbar.css'

const links = [
  { to: '/', label: '🫀 Home' },
  { to: '/predict', label: '🔬 Predict Risk' },
  { to: '/statistics', label: '📊 Statistics' },
  { to: '/about', label: 'ℹ️ About' },
]

export default function Navbar() {
  const { pathname } = useLocation()
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
    setOpen(false)
  }

  const close = () => setOpen(false)

  return (
    <nav className="navbar">
      <div className="navbar-top">
        <Link to="/" className="navbar-brand" onClick={close}>🫀 HeartGuard</Link>
        <button className="hamburger" onClick={() => setOpen(!open)} aria-label="Menu">
          <span className={`ham-line ${open ? 'open' : ''}`} />
          <span className={`ham-line ${open ? 'open' : ''}`} />
          <span className={`ham-line ${open ? 'open' : ''}`} />
        </button>
      </div>
      <ul className={`navbar-links ${open ? 'show' : ''}`}>
        {links.map(l => (
          <li key={l.to}>
            <Link to={l.to} className={pathname === l.to ? 'active' : ''} onClick={close}>{l.label}</Link>
          </li>
        ))}
        {user && (
          <li>
            <Link to="/lifestyle" className={pathname === '/lifestyle' ? 'active' : ''} onClick={close}>🏃 Lifestyle</Link>
          </li>
        )}
        <li>
          {user ? (
            <button className="nav-auth-btn" onClick={handleLogout}>👋 Logout</button>
          ) : (
            <Link to="/login" className={`nav-auth-link ${pathname === '/login' ? 'active' : ''}`} onClick={close}>🔐 Login</Link>
          )}
        </li>
      </ul>
    </nav>
  )
}
