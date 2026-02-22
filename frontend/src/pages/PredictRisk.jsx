import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import './PredictRisk.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
const API_URL = `${API_BASE}/api/predict`

const cpOptions = [
  { label: 'Asymptomatic (No chest pain)', value: 0 },
  { label: 'Atypical Angina', value: 1 },
  { label: 'Non-Anginal Pain', value: 2 },
  { label: 'Typical Angina', value: 3 },
]
const restecgOptions = [
  { label: 'Normal', value: 0 },
  { label: 'ST-T Wave Abnormality', value: 1 },
  { label: 'Left Ventricular Hypertrophy', value: 2 },
]
const slopeOptions = [
  { label: 'Downsloping', value: 0 },
  { label: 'Flat', value: 1 },
  { label: 'Upsloping', value: 2 },
]
const thallOptions = [
  { label: 'Normal', value: 2 },
  { label: 'Fixed Defect', value: 1 },
  { label: 'Reversible Defect', value: 3 },
  { label: 'Unknown', value: 0 },
]

const testPresets = [
  {
    label: '💚 35yo Male — No Risk (cp=Asymptomatic, thall=Reversible Defect)',
    data: { age: 35, sex: 1, cp: 0, trtbps: 120, chol: 198, fbs: 0, restecg: 1, thalachh: 130, exng: 1, oldpeak: 1.6, slp: 1, caa: 0, thall: 3 },
  },
  {
    label: '💚 39yo Male — No Risk (cp=Asymptomatic, thall=Reversible Defect)',
    data: { age: 39, sex: 1, cp: 0, trtbps: 118, chol: 219, fbs: 0, restecg: 1, thalachh: 140, exng: 0, oldpeak: 1.2, slp: 1, caa: 0, thall: 3 },
  },
  {
    label: '⚠️ 63yo Male — High Risk (cp=Typical Angina, thall=Fixed Defect)',
    data: { age: 63, sex: 1, cp: 3, trtbps: 145, chol: 233, fbs: 1, restecg: 0, thalachh: 150, exng: 0, oldpeak: 2.3, slp: 0, caa: 0, thall: 1 },
  },
  {
    label: '⚠️ 39yo Female — High Risk (cp=Non-Anginal, thall=Normal)',
    data: { age: 39, sex: 0, cp: 2, trtbps: 94, chol: 199, fbs: 0, restecg: 1, thalachh: 179, exng: 0, oldpeak: 0, slp: 2, caa: 0, thall: 2 },
  },
]

// Framer Motion variants for step transitions
const stepVariants = {
  enter: (direction) => ({
    x: direction > 0 ? 50 : -50,
    opacity: 0,
    filter: 'blur(4px)'
  }),
  center: {
    zIndex: 1,
    x: 0,
    opacity: 1,
    filter: 'blur(0px)'
  },
  exit: (direction) => ({
    zIndex: 0,
    x: direction < 0 ? 50 : -50,
    opacity: 0,
    filter: 'blur(4px)'
  })
}

export default function PredictRisk() {
  const { user, token } = useAuth()
  const [form, setForm] = useState({
    age: 45, sex: 1, cp: 0, trtbps: 120, chol: 200,
    fbs: 0, restecg: 0, thalachh: 150, exng: 0,
    oldpeak: 1.0, slp: 1, caa: 0, thall: 2,
  })

  // Wizard State
  const [[step, direction], setPage] = useState([1, 0])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [stage, setStage] = useState('')
  const [error, setError] = useState('')

  const paginate = (newDirection) => {
    setPage([step + newDirection, newDirection])
  }

  const set = (key, raw) => {
    const v = typeof raw === 'string' ? (raw.includes('.') ? parseFloat(raw) : parseInt(raw, 10)) : raw
    setForm(prev => ({ ...prev, [key]: isNaN(v) ? raw : v }))
  }

  const applyPreset = (index) => {
    if (index === '') return
    setForm(testPresets[index].data)
    setResult(null)
    setError('')
    setPage([1, -1]) // reset to first step on preset
  }

  const predict = async () => {
    setError('')
    setResult(null)
    setLoading(true)
    setPage([4, 1]) // Move to loading step

    const stages = [
      '🔄 Preparing neural pathways...',
      '📡 Parsing biometrics...',
      '🫀 Simulating cardiovascular models...',
      '🧬 Cross-referencing risk factors...',
      '✨ Finalizing prediction...',
    ]

    // Simulate complex thinking for UI
    for (const s of stages) {
      setStage(s)
      await new Promise(r => setTimeout(r, 600))
    }

    try {
      const headers = { 'Content-Type': 'application/json' }
      if (token) headers['Authorization'] = `Bearer ${token}`

      const res = await fetch(API_URL, {
        method: 'POST',
        headers,
        body: JSON.stringify(form),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Prediction failed')
      setResult(data)
      setPage([5, 1]) // Move to result step
    } catch (e) {
      setError(e.message)
      setPage([3, -1]) // back to form if error
    } finally {
      setLoading(false)
      setStage('')
    }
  }

  // Sub-components for steps to keep render clean
  const renderStepOne = () => (
    <div className="wizard-step">
      <h3 className="step-title">👤 Phase 1: Vitals & Baseline</h3>
      <div className="form-group-grid">
        <label>Age
          <input type="number" min={1} max={120} value={form.age} onChange={e => set('age', e.target.value)} />
        </label>
        <label>Sex
          <select value={form.sex} onChange={e => set('sex', e.target.value)}>
            <option value={1}>Male</option>
            <option value={0}>Female</option>
          </select>
        </label>
        <label>Resting BP <span className="help-text">mmHg</span>
          <input type="number" min={80} max={250} value={form.trtbps} onChange={e => set('trtbps', e.target.value)} />
        </label>
        <label>Max Heart Rate <span className="help-text">bpm</span>
          <input type="number" min={60} max={220} value={form.thalachh} onChange={e => set('thalachh', e.target.value)} />
        </label>
      </div>
      <div className="range-group">
        <label>Cholesterol ({form.chol} mg/dl)</label>
        <input type="range" min={100} max={600} step={5} value={form.chol} onChange={e => set('chol', e.target.value)} />
      </div>
    </div>
  )

  const renderStepTwo = () => (
    <div className="wizard-step">
      <h3 className="step-title">🩺 Phase 2: Symptoms & History</h3>
      <div className="form-group-grid">
        <label>Chest Pain Type
          <select value={form.cp} onChange={e => set('cp', e.target.value)}>
            {cpOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </label>
        <label>Exercise Angina?
          <select value={form.exng} onChange={e => set('exng', e.target.value)}>
            <option value={0}>No Pain</option>
            <option value={1}>Yes, Painful</option>
          </select>
        </label>
      </div>
      <div className="range-group">
        <label>ST Depression / Oldpeak ({form.oldpeak})</label>
        <input type="range" min={0} max={6} step={0.1} value={form.oldpeak} onChange={e => set('oldpeak', e.target.value)} />
      </div>
      <label className="checkbox-label">
        <input type="checkbox" checked={form.fbs === 1} onChange={e => set('fbs', e.target.checked ? 1 : 0)} />
        Fasting Blood Sugar &gt; 120 mg/dl
      </label>
    </div>
  )

  const renderStepThree = () => (
    <div className="wizard-step">
      <h3 className="step-title">🔬 Phase 3: Clinical Tests</h3>
      <div className="form-group-grid">
        <label>Resting ECG
          <select value={form.restecg} onChange={e => set('restecg', e.target.value)}>
            {restecgOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </label>
        <label>ST Slope
          <select value={form.slp} onChange={e => set('slp', e.target.value)}>
            {slopeOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </label>
        <label>Major Vessels Blocked
          <select value={form.caa} onChange={e => set('caa', e.target.value)}>
            {[0, 1, 2, 3].map(v => <option key={v} value={v}>{v}</option>)}
          </select>
        </label>
        <label>Thalassemia
          <select value={form.thall} onChange={e => set('thall', e.target.value)}>
            {thallOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </label>
      </div>
    </div>
  )

  const renderLoading = () => (
    <div className="wizard-loading">
      <div className="radar-scanner">
        <div className="radar-beam"></div>
      </div>
      <h3 className="loading-text animate-pulse">Scanning Biometrics...</h3>
      <p className="loading-stage">{stage}</p>
    </div>
  )

  const generateProtocol = async () => {
    setLoading(true)
    setStage('🧠 Groq AI is designing your custom 4-week protocol...')
    setPage([4, 1]) // Switch back to the loading radar

    try {
      const authHeader = { 'Authorization': `Bearer ${token || ''}` }
      const res = await fetch(`${API_BASE}/api/ai/protocol`, {
        method: 'POST',
        headers: authHeader
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed to generate protocol')

      // Successfully generated. Proceed to dashboard!
      window.location.href = '/lifestyle'
    } catch (e) {
      setError(e.message)
      setPage([5, -1]) // Go back to result on error
      setLoading(false)
      setStage('')
    }
  }

  const renderResult = () => (
    <div className={`result-card-v2 ${result.prediction === 0 ? 'result-safe' : 'result-risk'}`}>
      <div className="result-header">
        <div className="result-icon-lg">{result.prediction === 0 ? '🛡️' : '⚠️'}</div>
        <h2 className="result-title-lg">{result.prediction === 0 ? 'Low Risk Profile' : 'High Risk Indicator'}</h2>
      </div>

      <p className="result-desc">
        {result.prediction === 0
          ? 'Your parameters align with a healthy cardiovascular profile. Excellent work maintaining these markers.'
          : 'Our AI has detected patterns that correlate with an elevated risk of heart disease.'}
      </p>

      <div className="confidence-meter">
        <div className="meter-label">
          <span>AI Confidence</span>
          <span>{result.confidence}%</span>
        </div>
        <div className="meter-track">
          <motion.div
            className="meter-fill"
            initial={{ width: 0 }}
            animate={{ width: `${result.confidence}%` }}
            transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
          />
        </div>
      </div>

      <div className="result-actions">
        {user ? (
          <button className="btn-primary" onClick={generateProtocol} disabled={loading}>
            ✨ Generate AI Protocol & Go To Dashboard
          </button>
        ) : (
          <Link to="/login" className="btn-primary">
            📋 Sign up to Track Goals
          </Link>
        )}
        <button className="btn-secondary" onClick={() => { setPage([1, -1]); setResult(null); }}>
          Retest
        </button>
      </div>
    </div>
  )

  return (
    <div className="predict-page">
      <div className="predict-header text-center">
        <h1 className="page-title">Heart Risk AI Core</h1>
        <p className="page-subtitle">Precision diagnostics powered by machine learning</p>

        {step < 4 && (
          <div className="wizard-progress">
            <div className={`progress-pip ${step >= 1 ? 'active' : ''}`}>1. Vitals</div>
            <div className="progress-line" />
            <div className={`progress-pip ${step >= 2 ? 'active' : ''}`}>2. History</div>
            <div className="progress-line" />
            <div className={`progress-pip ${step >= 3 ? 'active' : ''}`}>3. Tests</div>
          </div>
        )}
      </div>

      {error && <div className="warning-banner" style={{ justifyContent: 'center' }}>❌ {error}</div>}

      <div className="wizard-container glass-card">
        <AnimatePresence initial={false} custom={direction} mode="wait">
          <motion.div
            key={step}
            custom={direction}
            variants={stepVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ type: "tween", ease: "easeInOut", duration: 0.3 }}
            className="wizard-content"
          >
            {step === 1 && renderStepOne()}
            {step === 2 && renderStepTwo()}
            {step === 3 && renderStepThree()}
            {step === 4 && renderLoading()}
            {step === 5 && renderResult()}
          </motion.div>
        </AnimatePresence>

        {step < 4 && (
          <div className="wizard-controls">
            <button
              className="btn-secondary"
              onClick={() => paginate(-1)}
              disabled={step === 1}
              style={{ opacity: step === 1 ? 0 : 1 }}
            >
              ← Back
            </button>

            {step < 3 ? (
              <button className="btn-primary" onClick={() => paginate(1)}>
                Next Phase →
              </button>
            ) : (
              <button className="btn-primary submit-btn" onClick={predict} disabled={loading}>
                🚀 Initialize AI Core
              </button>
            )}
          </div>
        )}
      </div>

      {step < 4 && (
        <div className="preset-bar-hz">
          <span className="preset-label">Quick Demographics:</span>
          <select className="preset-select-glass" defaultValue="" onChange={e => applyPreset(e.target.value)}>
            <option value="" disabled>Load Test Case...</option>
            {testPresets.map((p, i) => <option key={i} value={i}>{p.label}</option>)}
          </select>
        </div>
      )}
    </div>
  )
}

