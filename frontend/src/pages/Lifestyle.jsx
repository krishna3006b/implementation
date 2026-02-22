import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
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

const HabitSpark = ({ streak, completionPct }) => {
    let sparkClass = 'spark-0'
    let sparkTitle = 'Spark is sleeping. Complete goals to wake it up!'
    if (streak >= 7) {
        sparkClass = 'spark-3'
        sparkTitle = 'Spark is blazing! You are unstoppable!'
    } else if (streak >= 3) {
        sparkClass = 'spark-2'
        sparkTitle = 'Spark is glowing! Keep the momentum!'
    } else if (streak >= 1 || completionPct >= 80) {
        sparkClass = 'spark-1'
        sparkTitle = 'Spark is awakening. Stay consistent!'
    }

    return (
        <div className={`habit-spark-container`} title={sparkTitle}>
            <div className={`habit-spark ${sparkClass}`}>
                <div className="spark-core"></div>
                <div className="spark-aura"></div>
                <div className="spark-particles">✧</div>
            </div>
        </div>
    )
}

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
    const [quest, setQuest] = useState(null)
    const [questLoading, setQuestLoading] = useState(false)
    const [chatOpen, setChatOpen] = useState(false)
    const [chatMessages, setChatMessages] = useState([])
    const [chatInput, setChatInput] = useState('')
    const [chatLoading, setChatLoading] = useState(false)
    const chatEndRef = useRef(null)
    const saveTimer = useRef(null)

    // Voice-First Logging states
    const [listening, setListening] = useState(false)
    const [transcript, setTranscript] = useState('')
    const [voiceLoading, setVoiceLoading] = useState(false)

    // AI Persona states
    const [persona, setPersona] = useState('supportive')
    const [personas, setPersonas] = useState([])
    const [personaLoading, setPersonaLoading] = useState(false)

    const headers = useMemo(() => ({ Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }), [token])

    const fetchAll = useCallback(async () => {
        try {
            const [goalsRes, streakRes, logsRes] = await Promise.all([
                fetch(`${API_BASE}/api/goals`, { headers }),
                fetch(`${API_BASE}/api/tracker/streak`, { headers }),
                fetch(`${API_BASE}/api/tracker?days=60`, { headers }),
            ])
            const goalsData = await goalsRes.json()
            const streakData = await streakRes.json()
            const logsData = await logsRes.json()

            setGoals(goalsData.goals || [])
            setStreak(streakData)
            setCalendarLogs(logsData.logs || [])

            // Use IST (UTC+5:30) to match backend date calculations
            const now = new Date()
            const istOffset = 5.5 * 60 * 60 * 1000
            const istDate = new Date(now.getTime() + istOffset)
            const today = istDate.toISOString().slice(0, 10)
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
                fetch(`${API_BASE}/api/tracker?days=60`, { headers }),
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

    const fetchQuest = useCallback(async () => {
        setQuestLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/ai/quest`, { method: 'POST', headers })
            const data = await res.json()
            if (data.quest) {
                setQuest({ ...data.quest, completed: data.completed })
            }
        } catch (e) { console.error('Failed to fetch quest:', e) }
        finally { setQuestLoading(false) }
    }, [headers])

    useEffect(() => {
        // Fetch the daily quest automatically when page loads
        if (token) fetchQuest()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [token])

    useEffect(() => {
        const loadPersonas = async () => {
            try {
                const res = await fetch(`${API_BASE}/api/ai/persona`, { headers })
                const data = await res.json()
                setPersonas(data.personas || [])
                setPersona(data.current || 'supportive')
            } catch (e) { console.error('Failed to fetch personas:', e) }
        }
        if (token) loadPersonas()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [token])

    const completeQuest = async () => {
        if (!quest || quest.completed) return

        // Optimistically complete
        setQuest({ ...quest, completed: true })

        // Trigger massive confetti
        import('canvas-confetti').then((confetti) => {
            const duration = 3000;
            const end = Date.now() + duration;

            (function frame() {
                confetti.default({
                    particleCount: 5,
                    angle: 60,
                    spread: 55,
                    origin: { x: 0 },
                    colors: ['#ffeb3b', '#ff6b9d', '#00f0ff']
                });
                confetti.default({
                    particleCount: 5,
                    angle: 120,
                    spread: 55,
                    origin: { x: 1 },
                    colors: ['#ffeb3b', '#ff6b9d', '#00f0ff']
                });

                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            }());
        });

        try {
            await fetch(`${API_BASE}/api/ai/quest/complete`, { method: 'POST', headers })
        } catch (e) {
            console.error('Failed to complete quest:', e)
        }
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

    const buildHeatmap = () => {
        const cells = []
        const logMap = {}
        calendarLogs.forEach(l => { logMap[l.date] = l })
        const istOffset = 5.5 * 60 * 60 * 1000

        for (let i = 59; i >= 0; i--) {
            const d = new Date()
            d.setDate(d.getDate() - i)
            const istDate = new Date(d.getTime() + istOffset)
            const dateStr = istDate.toISOString().slice(0, 10)
            cells.push({ date: dateStr, log: logMap[dateStr] || null })
        }
        return cells
    }

    const getHeatColor = (pct) => {
        if (!pct || pct === 0) return 'heat-0'
        if (pct < 50) return 'heat-1'
        if (pct < 80) return 'heat-2'
        return 'heat-3'
    }

    const useStreakFreeze = async () => {
        if (!streak.freezes || streak.freezes <= 0) return
        try {
            const res = await fetch(`${API_BASE}/api/tracker/streak/freeze`, {
                method: 'POST', headers,
            })
            const data = await res.json()
            if (data.success) {
                const streakRes = await fetch(`${API_BASE}/api/tracker/streak`, { headers })
                const streakData = await streakRes.json()
                setStreak(streakData)
                alert(`🧊 Streak Freeze used for ${data.date_frozen}! Your streak is protected.`)
            } else {
                alert(data.error || 'Could not use freeze.')
            }
        } catch (e) {
            console.error('Failed to use freeze:', e)
        }
    }

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

    // Voice-First Logging
    const startVoiceLog = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        if (!SpeechRecognition) {
            alert('Speech recognition is not supported in your browser. Try Chrome.')
            return
        }
        const recognition = new SpeechRecognition()
        recognition.lang = 'en-US'
        recognition.continuous = false
        recognition.interimResults = false
        recognition.maxAlternatives = 1

        setListening(true)
        setTranscript('')

        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript
            setTranscript(text)
            setListening(false)
            sendTranscript(text)
        }

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error)
            setListening(false)
            if (event.error === 'not-allowed') {
                alert('Microphone access denied. Please allow microphone permissions in your browser settings.')
            } else if (event.error === 'no-speech') {
                alert('No speech detected. Please try again and speak clearly.')
            }
        }

        recognition.onend = () => setListening(false)

        try {
            recognition.start()
        } catch (e) {
            console.error('Failed to start recognition:', e)
            setListening(false)
        }
    }

    const sendTranscript = async (text) => {
        setVoiceLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/ai/parse-log`, {
                method: 'POST', headers,
                body: JSON.stringify({ transcript: text }),
            })
            const data = await res.json()
            if (data.parsed) {
                const p = data.parsed
                if (p.completed) setCompleted(prev => [...new Set([...prev, ...p.completed])])
                if (p.values) setValues(prev => ({ ...prev, ...p.values }))
                if (p.mood) setMood(p.mood)
                if (p.energy) setEnergy(p.energy)
                if (p.notes) setNotes(prev => prev ? prev + '\n' + p.notes : p.notes)
                // Auto-save after voice parse
                setTimeout(() => {
                    saveTracking(
                        p.completed ? [...new Set([...completed, ...p.completed])] : completed,
                        p.values ? { ...values, ...p.values } : values,
                        p.mood || mood,
                        p.energy || energy,
                        p.notes ? (notes ? notes + '\n' + p.notes : p.notes) : notes
                    )
                }, 300)
            }
        } catch (e) {
            console.error('Voice parse failed:', e)
        } finally {
            setVoiceLoading(false)
        }
    }

    // AI Persona
    const fetchPersonas = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/ai/persona`, { headers })
            const data = await res.json()
            setPersonas(data.personas || [])
            setPersona(data.current || 'supportive')
        } catch (e) { console.error('Failed to fetch personas:', e) }
    }

    const setPersonaChoice = async (id) => {
        setPersonaLoading(true)
        try {
            await fetch(`${API_BASE}/api/ai/persona`, {
                method: 'POST', headers,
                body: JSON.stringify({ persona: id }),
            })
            setPersona(id)
            setAiTip('') // Clear old tip so new persona generates fresh
        } catch (e) { console.error('Failed to set persona:', e) }
        finally { setPersonaLoading(false) }
    }

    // SVG ring params
    const ringR = 52
    const ringC = 2 * Math.PI * ringR
    const ringOffset = ringC - (completionPct / 100) * ringC

    const hour = new Date().getHours()
    const greeting = hour < 12 ? '☀️ Good Morning' : hour < 18 ? '🌤️ Good Afternoon' : '🌙 Good Evening'

    const sortedGoals = [...goals].sort((a, b) => {
        const aDone = completed.includes(a.id)
        const bDone = completed.includes(b.id)
        if (aDone === bDone) return 0
        return aDone ? 1 : -1
    })

    const todayIST = (() => { const n = new Date(); return new Date(n.getTime() + 5.5 * 60 * 60 * 1000).toISOString().slice(0, 10) })()
    const isToday = !selectedDay || selectedDay === todayIST

    return (
        <div className="lifestyle-page">
            <div className="lifestyle-header text-center">
                <h1 className="page-title">{greeting}, {user?.name?.split(' ')[0] || 'Warrior'}</h1>
                <p className="page-subtitle">Your personalized daily health briefing</p>
            </div>

            {/* Daily Briefing Hero Section */}
            {isToday ? (
                <>
                    <div className="daily-briefing-glass">
                        <div className="briefing-content">
                            <div className="ai-coach-header">
                                <span className="ai-badge">🤖 Core AI Assistant</span>
                                <div className="persona-selector">
                                    {personas.map(p => (
                                        <button
                                            key={p.id}
                                            className={`persona-btn ${persona === p.id ? 'active' : ''}`}
                                            onClick={() => setPersonaChoice(p.id)}
                                            disabled={personaLoading}
                                            title={p.name}
                                        >
                                            {p.emoji}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            {aiTip ? (
                                <div className="ai-tip-content">
                                    <p>"{aiTip}"</p>
                                    <button className="ai-btn-small" onClick={fetchCoachTip} disabled={aiTipLoading}>
                                        {aiTipLoading ? '⏳ Recalculating...' : '🔄 Update Briefing'}
                                    </button>
                                </div>
                            ) : (
                                <div className="ai-tip-placeholder">
                                    <p>I can analyze your vitals and today's targets to create your action plan.</p>
                                    <button className="ai-btn" onClick={fetchCoachTip} disabled={aiTipLoading}>
                                        {aiTipLoading ? '⏳ Analyzing Bio-data...' : '✨ Generate Daily Briefing'}
                                    </button>
                                </div>
                            )}
                        </div>

                        <div className="briefing-stats">
                            <div className="completion-ring-wrap">
                                <svg viewBox="0 0 120 120" className="completion-ring">
                                    <circle cx="60" cy="60" r={ringR} stroke="rgba(255,255,255,0.06)" strokeWidth="8" fill="none" />
                                    <circle
                                        cx="60" cy="60" r={ringR}
                                        stroke={completionPct >= 80 ? 'var(--neon-cyan)' : completionPct >= 50 ? 'var(--yellow)' : 'var(--neon-pink)'}
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

                            <div className="streak-briefing">
                                <HabitSpark streak={streak.current_streak} completionPct={completionPct} />
                                <div className="streak-msg">{streakMessage}</div>
                                <div className="streak-bar-mini">
                                    <div className="streak-item-mini" title="Current Day Streak">
                                        <span className="streak-number-mini">{streak.current_streak}</span>
                                        <span className="streak-label-mini">🔥</span>
                                    </div>
                                    <div className="streak-item-mini" title="Best Streak">
                                        <span className="streak-number-mini">{streak.longest_streak}</span>
                                        <span className="streak-label-mini">🏆</span>
                                    </div>
                                    <div
                                        className={`streak-item-mini freeze-item ${streak.freezes > 0 ? 'has-freezes' : ''}`}
                                        title={streak.freezes > 0 ? 'Click to use a Streak Freeze for yesterday' : 'Earn freezes by reaching 7-day streaks'}
                                        onClick={streak.freezes > 0 ? useStreakFreeze : undefined}
                                        style={streak.freezes > 0 ? { cursor: 'pointer' } : {}}
                                    >
                                        <span className="streak-number-mini">{streak.freezes || 0}</span>
                                        <span className="streak-label-mini">🧊</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Daily Quest Gamification */}
                    {quest && (
                        <div className={`quest-card ${quest.completed ? 'quest-done' : ''}`}>
                            <div className="quest-header">
                                <span className="quest-badge">✨ Daily Quest</span>
                                <span className="quest-xp">+{quest.xp_reward || 50} XP</span>
                            </div>
                            <div className="quest-body">
                                <span className="quest-icon-lg">{quest.icon || '⭐'}</span>
                                <div className="quest-info">
                                    <h3>{quest.title || 'Daily Quest'}</h3>
                                    <p>{quest.description || 'Complete this task for a little health boost.'}</p>
                                </div>
                                <button
                                    className={`quest-action-btn ${quest.completed ? 'completed' : ''}`}
                                    onClick={completeQuest}
                                    disabled={quest.completed}
                                >
                                    {quest.completed ? '✓ Claimed' : 'Complete Quest'}
                                </button>
                            </div>
                        </div>
                    )}
                </>
            ) : (
                <div className="historical-warning glass-card">
                    <span className="warning-icon">🕰️</span>
                    <div className="warning-text">
                        <h3>Viewing Historical Data</h3>
                        <p>You are looking at {new Date(selectedDay + 'T00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}. Historical logs cannot be edited.</p>
                    </div>
                    <button className="return-today-btn" onClick={() => {
                        setSelectedDay(null)
                        const today = new Date().toISOString().slice(0, 10)
                        const log = calendarLogs.find(l => l.date === today)
                        setCompleted(log?.completed || [])
                        setValues(log?.values || {})
                        setMood(log?.mood || null)
                        setEnergy(log?.energy || 0)
                        setNotes(log?.notes || '')
                    }}>Return to Today</button>
                </div>
            )
            }

            {/* Today's Goals — Rich Cards */}
            <h2 className="section-title">
                Today's Goals
                <span className="pct-badge">{completed.length}/{goals.length}</span>
                {saving && <span className="save-indicator">💾 Saving...</span>}
            </h2>

            <div className="goals-grid-v2">
                {sortedGoals.map(g => {
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

            {/* Voice-First Quick Log */}
            <div className="voice-log-section">
                <button
                    className={`voice-mic-btn ${listening ? 'listening' : ''} ${voiceLoading ? 'processing' : ''}`}
                    onClick={startVoiceLog}
                    disabled={listening || voiceLoading}
                >
                    {listening ? '🔴' : voiceLoading ? '⏳' : '🎙️'}
                </button>
                <span className="voice-label">
                    {listening ? 'Listening... speak now!' : voiceLoading ? 'AI is parsing your update...' : 'Tap mic to log by voice'}
                </span>
                {transcript && <p className="voice-transcript">"{transcript}"</p>}
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
            <h2 className="section-title">📆 Consistency Heatmap</h2>

            <div className="github-heatmap-container">
                <div className="github-heatmap">
                    {buildHeatmap().map((cell, i) => (
                        <div
                            key={i}
                            className={`heatmap-cell ${getHeatColor(cell.log?.completion_pct)} ${selectedDay === cell.date ? 'selected' : ''}`}
                            onClick={() => setSelectedDay(selectedDay === cell.date ? null : cell.date)}
                            title={`${new Date(cell.date + 'T00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}: ${cell.log ? cell.log.completion_pct + '% completed' : 'No data'}`}
                        />
                    ))}
                </div>
            </div>
            <div className="heat-legend">
                <span>Less</span>
                <div className="heat-box heat-0" /><div className="heat-box heat-1" /><div className="heat-box heat-2" /><div className="heat-box heat-3" />
                <span>More</span>
            </div>

            {
                selectedDay && (() => {
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
                })()
            }

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
        </div >
    )
}
