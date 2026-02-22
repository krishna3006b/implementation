import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import './Lifestyle.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'

export default function Lifestyle() {
    const { user, token } = useAuth()
    const [goals, setGoals] = useState([])
    const [completed, setCompleted] = useState([])
    const [streak, setStreak] = useState({ current_streak: 0, longest_streak: 0, total_days_tracked: 0 })
    const [calendarLogs, setCalendarLogs] = useState([])
    const [currentMonth, setCurrentMonth] = useState(() => {
        const d = new Date()
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    })
    const [loading, setLoading] = useState(true)
    const [selectedDay, setSelectedDay] = useState(null)

    const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

    const fetchAll = useCallback(async () => {
        try {
            const [goalsRes, streakRes, logsRes] = await Promise.all([
                fetch(`${API_BASE}/api/goals`, { headers }),
                fetch(`${API_BASE}/api/tracker/streak`, { headers }),
                fetch(`${API_BASE}/api/tracker?month=${currentMonth}`, { headers }),
            ])
            const goalsData = await goalsRes.json()
            const streakData = await streakRes.json()
            const logsData = await logsRes.json()

            setGoals(goalsData.goals || [])
            setStreak(streakData)
            setCalendarLogs(logsData.logs || [])

            // Find today's completed goals
            const today = new Date().toISOString().slice(0, 10)
            const todayLog = (logsData.logs || []).find(l => l.date === today)
            setCompleted(todayLog?.completed || [])
        } catch (e) {
            console.error('Failed to fetch data:', e)
        } finally {
            setLoading(false)
        }
    }, [token, currentMonth])

    useEffect(() => { fetchAll() }, [fetchAll])

    const toggleGoal = async (goalId) => {
        const updated = completed.includes(goalId)
            ? completed.filter(id => id !== goalId)
            : [...completed, goalId]
        setCompleted(updated)

        await fetch(`${API_BASE}/api/tracker/today`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ completed: updated }),
        })

        // Refresh streak + calendar
        const [streakRes, logsRes] = await Promise.all([
            fetch(`${API_BASE}/api/tracker/streak`, { headers }),
            fetch(`${API_BASE}/api/tracker?month=${currentMonth}`, { headers }),
        ])
        setStreak(await streakRes.json())
        const logsData = await logsRes.json()
        setCalendarLogs(logsData.logs || [])
    }

    const changeMonth = (delta) => {
        const [y, m] = currentMonth.split('-').map(Number)
        const d = new Date(y, m - 1 + delta, 1)
        setCurrentMonth(`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`)
        setSelectedDay(null)
    }

    // Build calendar grid
    const buildCalendar = () => {
        const [year, month] = currentMonth.split('-').map(Number)
        const firstDay = new Date(year, month - 1, 1).getDay()
        const daysInMonth = new Date(year, month, 0).getDate()
        const logMap = {}
        calendarLogs.forEach(l => { logMap[l.date] = l })

        const cells = []
        for (let i = 0; i < firstDay; i++) cells.push(null)
        for (let d = 1; d <= daysInMonth; d++) {
            const dateStr = `${currentMonth}-${String(d).padStart(2, '0')}`
            cells.push({ day: d, date: dateStr, log: logMap[dateStr] || null })
        }
        return cells
    }

    const getHeatColor = (pct) => {
        if (!pct || pct === 0) return 'heat-0'
        if (pct < 50) return 'heat-1'
        if (pct < 80) return 'heat-2'
        return 'heat-3'
    }

    const monthLabel = (() => {
        const [y, m] = currentMonth.split('-').map(Number)
        return new Date(y, m - 1).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
    })()

    const streakMessage = streak.current_streak >= 30 ? '🏆 Legendary! Keep it going!'
        : streak.current_streak >= 14 ? '🔥 On fire! Two week streak!'
            : streak.current_streak >= 7 ? '⭐ Amazing! One week streak!'
                : streak.current_streak >= 3 ? '💪 Good momentum! Keep pushing!'
                    : streak.current_streak >= 1 ? '🌱 Great start! Stay consistent!'
                        : '🎯 Complete 80%+ of your goals today to start a streak!'

    if (loading) return <div style={{ textAlign: 'center', padding: '4rem', color: '#aaa' }}>Loading your dashboard...</div>

    const completionPct = goals.length > 0 ? Math.round((completed.length / goals.length) * 100) : 0

    return (
        <div className="lifestyle-page">
            <h1 className="page-title">🏃 Lifestyle Dashboard</h1>
            <p className="page-subtitle">Hey {user?.name?.split(' ')[0]}! Track your daily health goals</p>

            {/* Streak Section */}
            <div className="streak-bar">
                <div className="streak-item">
                    <span className="streak-number">{streak.current_streak}</span>
                    <span className="streak-label">🔥 Current Streak</span>
                </div>
                <div className="streak-item">
                    <span className="streak-number">{streak.longest_streak}</span>
                    <span className="streak-label">🏆 Best Streak</span>
                </div>
                <div className="streak-item">
                    <span className="streak-number">{streak.total_days_tracked}</span>
                    <span className="streak-label">📅 Days Tracked</span>
                </div>
            </div>
            <div className="streak-msg">{streakMessage}</div>

            {/* Today's Goals */}
            <h2 className="section-title">Today's Goals <span className="pct-badge">{completionPct}%</span></h2>
            <div className="goals-grid">
                {goals.map(g => (
                    <button
                        key={g.id}
                        className={`goal-card ${completed.includes(g.id) ? 'done' : ''}`}
                        onClick={() => toggleGoal(g.id)}
                    >
                        <span className="goal-icon">{g.icon}</span>
                        <span className="goal-label">{g.label}</span>
                        <span className="goal-check">{completed.includes(g.id) ? '✅' : '⬜'}</span>
                    </button>
                ))}
            </div>

            {/* Calendar Heatmap */}
            <h2 className="section-title">📆 Activity Calendar</h2>
            <div className="calendar-nav">
                <button onClick={() => changeMonth(-1)}>← Prev</button>
                <span className="month-label">{monthLabel}</span>
                <button onClick={() => changeMonth(1)}>Next →</button>
            </div>

            <div className="calendar-header">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
                    <div key={d} className="cal-day-name">{d}</div>
                ))}
            </div>
            <div className="calendar-grid">
                {buildCalendar().map((cell, i) =>
                    cell ? (
                        <div
                            key={i}
                            className={`cal-cell ${getHeatColor(cell.log?.completion_pct)} ${selectedDay === cell.date ? 'selected' : ''}`}
                            onClick={() => setSelectedDay(selectedDay === cell.date ? null : cell.date)}
                            title={cell.log ? `${cell.log.completion_pct}% completed` : 'No data'}
                        >
                            {cell.day}
                        </div>
                    ) : (
                        <div key={i} className="cal-cell empty" />
                    )
                )}
            </div>

            <div className="heat-legend">
                <span>Less</span>
                <div className="heat-box heat-0" />
                <div className="heat-box heat-1" />
                <div className="heat-box heat-2" />
                <div className="heat-box heat-3" />
                <span>More</span>
            </div>

            {selectedDay && (() => {
                const log = calendarLogs.find(l => l.date === selectedDay)
                return (
                    <div className="day-detail">
                        <h3>📋 {new Date(selectedDay + 'T00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}</h3>
                        {log ? (
                            <>
                                <p className="detail-pct">{log.completion_pct}% completed ({log.completed?.length || 0}/{log.total_goals} goals)</p>
                                <div className="detail-tags">
                                    {goals.map(g => (
                                        <span key={g.id} className={`tag ${log.completed?.includes(g.id) ? 'tag-done' : 'tag-miss'}`}>
                                            {g.icon} {g.label}
                                        </span>
                                    ))}
                                </div>
                            </>
                        ) : (
                            <p className="detail-pct">No activity logged</p>
                        )}
                    </div>
                )
            })()}
        </div>
    )
}
