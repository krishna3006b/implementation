import { useState, useEffect, useCallback, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import './Lifestyle.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'

const MOODS = [
    { value: 'great', emoji: '😄', label: 'Great' },
    { value: 'good', emoji: '🙂', label: 'Good' },
    { value: 'okay', emoji: '😐', label: 'Okay' },
    { value: 'bad', emoji: '😞', label: 'Bad' },
    { value: 'terrible', emoji: '😣', label: 'Terrible' },
]

export default function Lifestyle() {
    const { user, token } = useAuth()
    const [goals, setGoals] = useState([])
    const [completed, setCompleted] = useState([])
    const [values, setValues] = useState({})
    const [mood, setMood] = useState(null)
    const [energy, setEnergy] = useState(0)
    const [notes, setNotes] = useState('')
    const [streak, setStreak] = useState({ current_streak: 0, longest_streak: 0, total_days_tracked: 0 })
    const [calendarLogs, setCalendarLogs] = useState([])
    const [currentMonth, setCurrentMonth] = useState(() => {
        const d = new Date()
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    })
    const [loading, setLoading] = useState(true)
    const [selectedDay, setSelectedDay] = useState(null)
    const [saving, setSaving] = useState(false)
    const [saved, setSaved] = useState(false)

    // AI states
    const [aiTip, setAiTip] = useState('')
    const [aiTipLoading, setAiTipLoading] = useState(false)
    const [aiInsights, setAiInsights] = useState('')
    const [aiInsightsLoading, setAiInsightsLoading] = useState(false)
    const [chatOpen, setChatOpen] = useState(false)
    const [chatMessages, setChatMessages] = useState([])
    const [chatInput, setChatInput] = useState('')
    const [chatLoading, setChatLoading] = useState(false)
    const chatEndRef = useRef(null)
    const saveTimer = useRef(null)

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

            const today = new Date().toISOString().slice(0, 10)
            const todayLog = (logsData.logs || []).find(l => l.date === today)
            setCompleted(todayLog?.completed || [])
            setValues(todayLog?.values || {})
            setMood(todayLog?.mood || null)
            setEnergy(todayLog?.energy || 0)
            setNotes(todayLog?.notes || '')
        } catch (e) {
            console.error('Failed to fetch data:', e)
        } finally {
            setLoading(false)
        }
    }, [token, currentMonth])

    useEffect(() => { fetchAll() }, [fetchAll])
    useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [chatMessages])

    // Debounced save
    const saveTracking = useCallback(async (newCompleted, newValues, newMood, newEnergy, newNotes) => {
        setSaving(true)
        try {
            await fetch(`${API_BASE}/api/tracker/today`, {
                method: 'POST', headers,
                body: JSON.stringify({
                    completed: newCompleted,
                    values: newValues,
                    mood: newMood,
                    energy: newEnergy,
                    notes: newNotes,
                }),
            })
            const [streakRes, logsRes] = await Promise.all([
                fetch(`${API_BASE}/api/tracker/streak`, { headers }),
                fetch(`${API_BASE}/api/tracker?month=${currentMonth}`, { headers }),
            ])
            setStreak(await streakRes.json())
            const logsData = await logsRes.json()
            setCalendarLogs(logsData.logs || [])
        } catch (e) {
            console.error('Save failed:', e)
        } finally {
            setSaving(false)
        }
    }, [token, currentMonth])

    const debouncedSave = (c, v, m, e, n) => {
        if (saveTimer.current) clearTimeout(saveTimer.current)
        saveTimer.current = setTimeout(() => saveTracking(c, v, m, e, n), 600)
    }

    const toggleGoal = (goalId) => {
        const wasCompleted = completed.includes(goalId)
        const newCompleted = wasCompleted
            ? completed.filter(id => id !== goalId)
            : [...completed, goalId]

        const goal = goals.find(g => g.id === goalId)
        const newValues = { ...values }

        if (!wasCompleted && goal && goal.target > 0 && !newValues[goalId]) {
            newValues[goalId] = goal.target
        }
        if (wasCompleted) {
            delete newValues[goalId]
        }

        setCompleted(newCompleted)
        setValues(newValues)
        debouncedSave(newCompleted, newValues, mood, energy, notes)
    }

    const updateValue = (goalId, val) => {
        const goal = goals.find(g => g.id === goalId)
        if (!goal) return
        const numVal = Math.max(0, parseFloat(val) || 0)
        const newValues = { ...values, [goalId]: numVal }

        let newCompleted = [...completed]
        if (goal.target > 0 && numVal >= goal.target && !newCompleted.includes(goalId)) {
            newCompleted.push(goalId)
        } else if (goal.target > 0 && numVal < goal.target && newCompleted.includes(goalId)) {
            newCompleted = newCompleted.filter(id => id !== goalId)
        }

        setValues(newValues)
        setCompleted(newCompleted)
        debouncedSave(newCompleted, newValues, mood, energy, notes)
    }

    const quickAdjust = (goalId, delta) => {
        const current = values[goalId] || 0
        const goal = goals.find(g => g.id === goalId)
        const step = goal?.unit === 'steps' ? 500 : goal?.unit === 'minutes' ? 5 : 0.5
        updateValue(goalId, current + delta * step)
    }

    const setMoodValue = (m) => {
        setMood(m)
        debouncedSave(completed, values, m, energy, notes)
    }

    const setEnergyValue = (e) => {
        setEnergy(e)
        debouncedSave(completed, values, mood, e, notes)
    }

    const saveNotes = () => {
        debouncedSave(completed, values, mood, energy, notes)
    }

    // AI functions
    const fetchCoachTip = async () => {
        setAiTipLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/ai/coach`, { method: 'POST', headers })
            const data = await res.json()
            setAiTip(data.tip || data.error || 'Unable to generate tip.')
        } catch { setAiTip('Failed to connect to AI coach.') }
        finally { setAiTipLoading(false) }
    }

    const fetchInsights = async () => {
        setAiInsightsLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/ai/insights`, { method: 'POST', headers })
            const data = await res.json()
            setAiInsights(data.insights || data.error || 'Unable to generate insights.')
        } catch { setAiInsights('Failed to connect to AI coach.') }
        finally { setAiInsightsLoading(false) }
    }

    const sendChat = async (e) => {
        e.preventDefault()
        if (!chatInput.trim() || chatLoading) return
        const msg = chatInput.trim()
        setChatInput('')
        const newMsgs = [...chatMessages, { role: 'user', content: msg }]
        setChatMessages(newMsgs)
        setChatLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/ai/chat`, {
                method: 'POST', headers,
                body: JSON.stringify({ message: msg, history: newMsgs.slice(-10) }),
            })
            const data = await res.json()
            setChatMessages(prev => [...prev, { role: 'assistant', content: data.reply || data.error || 'No response.' }])
        } catch {
            setChatMessages(prev => [...prev, { role: 'assistant', content: 'Failed to connect. Please try again.' }])
        } finally { setChatLoading(false) }
    }

    const changeMonth = (delta) => {
        const [y, m] = currentMonth.split('-').map(Number)
        const d = new Date(y, m - 1 + delta, 1)
        setCurrentMonth(`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`)
        setSelectedDay(null)
    }

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
    const isBinary = (g) => g.target === 0

    const quickChatSuggestions = [
        '🥗 Heart-healthy meal plan',
        '🏃 Exercise for my risk level',
        '😴 Tips to improve sleep',
        '🧘 Stress management techniques',
    ]

    // SVG ring params
    const ringR = 52
    const ringC = 2 * Math.PI * ringR
    const ringOffset = ringC - (completionPct / 100) * ringC

    return (
        <div className="lifestyle-page">
            <h1 className="page-title">🏃 Lifestyle Dashboard</h1>
            <p className="page-subtitle">Hey {user?.name?.split(' ')[0]}! Track your daily health goals</p>

            {/* Top Stats Row */}
            <div className="top-stats">
                {/* Completion Ring */}
                <div className="completion-ring-wrap">
                    <svg viewBox="0 0 120 120" className="completion-ring">
                        <circle cx="60" cy="60" r={ringR} stroke="rgba(255,255,255,0.06)" strokeWidth="8" fill="none" />
                        <circle
                            cx="60" cy="60" r={ringR}
                            stroke={completionPct >= 80 ? '#00ffaa' : completionPct >= 50 ? '#ffd866' : '#ff6b9d'}
                            strokeWidth="8" fill="none"
                            strokeLinecap="round"
                            strokeDasharray={ringC}
                            strokeDashoffset={ringOffset}
                            transform="rotate(-90 60 60)"
                            className="ring-progress"
                        />
                        <text x="60" y="55" textAnchor="middle" className="ring-pct">{completionPct}%</text>
                        <text x="60" y="72" textAnchor="middle" className="ring-label">done</text>
                    </svg>
                </div>

                {/* Streak */}
                <div className="streak-bar">
                    <div className="streak-item">
                        <span className="streak-number">{streak.current_streak}</span>
                        <span className="streak-label">🔥 Current</span>
                    </div>
                    <div className="streak-item">
                        <span className="streak-number">{streak.longest_streak}</span>
                        <span className="streak-label">🏆 Best</span>
                    </div>
                    <div className="streak-item">
                        <span className="streak-number">{streak.total_days_tracked}</span>
                        <span className="streak-label">📅 Days</span>
                    </div>
                </div>
            </div>
            <div className="streak-msg">{streakMessage}</div>

            {/* AI Coach Card */}
            <div className="ai-coach-card">
                <div className="ai-coach-header">
                    <span className="ai-badge">🤖 AI</span>
                    <h3>Your Personal Health Coach</h3>
                </div>
                {aiTip ? (
                    <div className="ai-tip-content">
                        <p>{aiTip}</p>
                        <button className="ai-btn-small" onClick={fetchCoachTip} disabled={aiTipLoading}>
                            {aiTipLoading ? '⏳ Thinking...' : '🔄 New Tip'}
                        </button>
                    </div>
                ) : (
                    <div className="ai-tip-placeholder">
                        <p>Get a personalized health tip based on your goals, streaks, and risk profile</p>
                        <button className="ai-btn" onClick={fetchCoachTip} disabled={aiTipLoading}>
                            {aiTipLoading ? '⏳ Analyzing your data...' : '✨ Get Today\'s Tip'}
                        </button>
                    </div>
                )}
            </div>

            {/* Today's Goals — Rich Cards */}
            <h2 className="section-title">
                Today's Goals
                <span className="pct-badge">{completed.length}/{goals.length}</span>
                {saving && <span className="save-indicator">💾 Saving...</span>}
            </h2>

            <div className="goals-grid-v2">
                {goals.map(g => {
                    const done = completed.includes(g.id)
                    const actual = values[g.id] || 0
                    const pct = isBinary(g) ? (done ? 100 : 0) : (g.target > 0 ? Math.min(Math.round((actual / g.target) * 100), 100) : 0)

                    return (
                        <div key={g.id} className={`goal-card-v2 ${done ? 'done' : ''}`}>
                            <div className="goal-top">
                                <span className="goal-icon-v2">{g.icon}</span>
                                <div className="goal-info">
                                    <span className="goal-name">{g.label}</span>
                                    {!isBinary(g) && (
                                        <span className="goal-target">{actual} / {g.target} {g.unit}</span>
                                    )}
                                </div>
                                <button
                                    className={`goal-check-v2 ${done ? 'checked' : ''}`}
                                    onClick={() => toggleGoal(g.id)}
                                    title={done ? 'Unmark' : 'Mark done'}
                                >
                                    {done ? '✓' : ''}
                                </button>
                            </div>

                            {!isBinary(g) ? (
                                <>
                                    <div className="goal-progress-bar">
                                        <div className="goal-progress-fill" style={{ width: `${pct}%` }} />
                                    </div>
                                    <div className="goal-controls">
                                        <button className="adj-btn" onClick={() => quickAdjust(g.id, -1)}>−</button>
                                        <input
                                            type="number"
                                            value={actual || ''}
                                            onChange={e => updateValue(g.id, e.target.value)}
                                            placeholder="0"
                                            className="goal-input"
                                        />
                                        <span className="goal-unit">{g.unit}</span>
                                        <button className="adj-btn" onClick={() => quickAdjust(g.id, 1)}>+</button>
                                    </div>
                                </>
                            ) : (
                                <div className="binary-toggle">
                                    <button
                                        className={`binary-btn ${done ? 'yes' : ''}`}
                                        onClick={() => { if (!done) toggleGoal(g.id) }}
                                    >✓ Yes</button>
                                    <button
                                        className={`binary-btn ${!done ? 'no' : ''}`}
                                        onClick={() => { if (done) toggleGoal(g.id) }}
                                    >✗ No</button>
                                </div>
                            )}
                        </div>
                    )
                })}
            </div>

            {/* Mood & Energy */}
            <div className="mood-energy-row">
                <div className="mood-section">
                    <h3>How are you feeling?</h3>
                    <div className="mood-options">
                        {MOODS.map(m => (
                            <button
                                key={m.value}
                                className={`mood-btn ${mood === m.value ? 'active' : ''}`}
                                onClick={() => setMoodValue(m.value)}
                                title={m.label}
                            >
                                <span className="mood-emoji">{m.emoji}</span>
                                <span className="mood-text">{m.label}</span>
                            </button>
                        ))}
                    </div>
                </div>
                <div className="energy-section">
                    <h3>Energy Level</h3>
                    <div className="energy-bar">
                        {[1, 2, 3, 4, 5].map(e => (
                            <button
                                key={e}
                                className={`energy-dot ${energy >= e ? 'active' : ''}`}
                                onClick={() => setEnergyValue(e)}
                            >
                                ⚡
                            </button>
                        ))}
                    </div>
                    <span className="energy-label">{energy > 0 ? `${energy}/5` : 'Tap to set'}</span>
                </div>
            </div>

            {/* Daily Notes */}
            <div className="daily-notes">
                <h3>📝 Daily Notes</h3>
                <textarea
                    value={notes}
                    onChange={e => setNotes(e.target.value)}
                    onBlur={saveNotes}
                    placeholder="How was your day? Any health observations, meals, activities..."
                    rows={3}
                />
            </div>

            {/* Save Button */}
            <div className="save-day-wrap">
                <button
                    className={`save-day-btn ${saved ? 'saved' : ''}`}
                    disabled={saving}
                    onClick={async () => {
                        setSaving(true)
                        setSaved(false)
                        if (saveTimer.current) clearTimeout(saveTimer.current)
                        await saveTracking(completed, values, mood, energy, notes)
                        setSaving(false)
                        setSaved(true)
                        setTimeout(() => setSaved(false), 2500)
                    }}
                >
                    {saving ? '💾 Saving...' : saved ? '✅ Saved Successfully!' : '💾 Save Today\'s Progress'}
                </button>
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
                <div className="heat-box heat-0" /><div className="heat-box heat-1" /><div className="heat-box heat-2" /><div className="heat-box heat-3" />
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
                                {log.mood && <p className="detail-mood">Mood: {MOODS.find(m => m.value === log.mood)?.emoji || ''} {log.mood} {log.energy ? `· Energy: ${'⚡'.repeat(log.energy)}` : ''}</p>}
                                {log.notes && <p className="detail-notes">"{log.notes}"</p>}
                                <div className="detail-tags">
                                    {goals.map(g => {
                                        const val = log.values?.[g.id]
                                        return (
                                            <span key={g.id} className={`tag ${log.completed?.includes(g.id) ? 'tag-done' : 'tag-miss'}`}>
                                                {g.icon} {g.label}{val != null ? ` (${val} ${g.unit})` : ''}
                                            </span>
                                        )
                                    })}
                                </div>
                            </>
                        ) : (
                            <p className="detail-pct">No activity logged</p>
                        )}
                    </div>
                )
            })()}

            {/* Weekly AI Insights */}
            <div className="ai-insights-section">
                <h2 className="section-title">📊 Weekly AI Insights</h2>
                {aiInsights ? (
                    <div className="ai-insights-content">
                        <div className="ai-insights-text">{aiInsights}</div>
                        <button className="ai-btn-small" onClick={fetchInsights} disabled={aiInsightsLoading}>
                            {aiInsightsLoading ? '⏳ Analyzing...' : '🔄 Refresh Analysis'}
                        </button>
                    </div>
                ) : (
                    <div className="ai-insights-placeholder">
                        <p>Get AI-powered analysis of your tracking patterns, habits, and personalized recommendations</p>
                        <button className="ai-btn" onClick={fetchInsights} disabled={aiInsightsLoading}>
                            {aiInsightsLoading ? '⏳ Analyzing your patterns...' : '🧠 Generate My Weekly Report'}
                        </button>
                    </div>
                )}
            </div>

            {/* AI Chat Widget */}
            <div className={`chat-widget ${chatOpen ? 'open' : ''}`}>
                <button className="chat-toggle" onClick={() => setChatOpen(!chatOpen)}>
                    {chatOpen ? '✕' : '💬'}
                    {!chatOpen && <span className="chat-toggle-label">Ask AI Coach</span>}
                </button>
                {chatOpen && (
                    <div className="chat-container">
                        <div className="chat-header">
                            <span className="ai-badge">🤖 AI</span>
                            <span>Health Coach Chat</span>
                        </div>
                        <div className="chat-messages">
                            {chatMessages.length === 0 && (
                                <div className="chat-welcome">
                                    <p>Hi {user?.name?.split(' ')[0]}! 👋 Ask me anything about heart health, diet, exercise, or lifestyle.</p>
                                    <div className="chat-suggestions">
                                        {quickChatSuggestions.map((s, i) => (
                                            <button key={i} className="suggestion-chip" onClick={() => setChatInput(s)}>
                                                {s}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}
                            {chatMessages.map((msg, i) => (
                                <div key={i} className={`chat-msg ${msg.role}`}>
                                    <div className="msg-bubble">{msg.content}</div>
                                </div>
                            ))}
                            {chatLoading && (
                                <div className="chat-msg assistant">
                                    <div className="msg-bubble typing">
                                        <span className="dot" /><span className="dot" /><span className="dot" />
                                    </div>
                                </div>
                            )}
                            <div ref={chatEndRef} />
                        </div>
                        <form className="chat-input-bar" onSubmit={sendChat}>
                            <input
                                type="text"
                                value={chatInput}
                                onChange={e => setChatInput(e.target.value)}
                                placeholder="Ask about diet, exercise, sleep..."
                                disabled={chatLoading}
                            />
                            <button type="submit" disabled={chatLoading || !chatInput.trim()}>→</button>
                        </form>
                    </div>
                )}
            </div>
        </div>
    )
}
