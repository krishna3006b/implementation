import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

const links = [
  { to: '/', label: '🫀 Home' },
  { to: '/predict', label: '🔬 Predict Risk' },
  { to: '/statistics', label: '📊 Statistics' },
  { to: '/about', label: 'ℹ️ About' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">🫀 HeartGuard</Link>
      <ul className="navbar-links">
        {links.map(l => (
          <li key={l.to}>
            <Link to={l.to} className={pathname === l.to ? 'active' : ''}>{l.label}</Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}
