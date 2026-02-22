import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Login.css'

export default function Login() {
    const [isSignup, setIsSignup] = useState(false)
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { login, signup } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            if (isSignup) {
                await signup(name, email, password)
            } else {
                await login(email, password)
            }
            navigate('/lifestyle')
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="login-page">
            <div className="login-card">
                <div className="login-icon">🫀</div>
                <h1>{isSignup ? 'Create Account' : 'Welcome Back'}</h1>
                <p className="login-sub">{isSignup ? 'Start your heart-healthy journey' : 'Track your daily lifestyle goals'}</p>

                <div className="tab-bar">
                    <button className={!isSignup ? 'active' : ''} onClick={() => setIsSignup(false)}>Login</button>
                    <button className={isSignup ? 'active' : ''} onClick={() => setIsSignup(true)}>Sign Up</button>
                </div>

                <form onSubmit={handleSubmit}>
                    {isSignup && (
                        <label>
                            Name
                            <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Your name" required />
                        </label>
                    )}
                    <label>
                        Email
                        <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@email.com" required />
                    </label>
                    <label>
                        Password
                        <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" required minLength={6} />
                    </label>

                    {error && <div className="login-error">❌ {error}</div>}

                    <button type="submit" className="btn-primary login-btn" disabled={loading}>
                        {loading ? '⏳ Please wait...' : isSignup ? '🚀 Create Account' : '🔓 Login'}
                    </button>
                </form>
            </div>
        </div>
    )
}
