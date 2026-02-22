import { useState } from 'react'
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
    label: '💚 Healthy Young Male (Low Risk)',
    data: { age: 35, sex: 1, cp: 0, trtbps: 126, chol: 282, fbs: 0, restecg: 0, thalachh: 156, exng: 1, oldpeak: 0, slp: 2, caa: 0, thall: 3 },
  },
  {
    label: '💚 Healthy Female (Low Risk)',
    data: { age: 39, sex: 0, cp: 2, trtbps: 94, chol: 199, fbs: 0, restecg: 1, thalachh: 179, exng: 0, oldpeak: 0, slp: 2, caa: 0, thall: 2 },
  },
  {
    label: '⚠️ Older Male with Angina (High Risk)',
    data: { age: 67, sex: 1, cp: 0, trtbps: 160, chol: 286, fbs: 0, restecg: 0, thalachh: 108, exng: 1, oldpeak: 1.5, slp: 1, caa: 3, thall: 2 },
  },
  {
    label: '⚠️ Male with High Oldpeak (High Risk)',
    data: { age: 55, sex: 1, cp: 0, trtbps: 140, chol: 217, fbs: 0, restecg: 1, thalachh: 111, exng: 1, oldpeak: 5.6, slp: 0, caa: 0, thall: 3 },
  },
]

export default function PredictRisk() {
  const [form, setForm] = useState({
    age: 45, sex: 1, cp: 0, trtbps: 120, chol: 200,
    fbs: 0, restecg: 0, thalachh: 150, exng: 0,
    oldpeak: 1.0, slp: 1, caa: 0, thall: 2,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [stage, setStage] = useState('')
  const [error, setError] = useState('')

  const set = (key, raw) => {
    const v = typeof raw === 'string' ? (raw.includes('.') ? parseFloat(raw) : parseInt(raw, 10)) : raw
    setForm(prev => ({ ...prev, [key]: isNaN(v) ? raw : v }))
  }

  const applyPreset = (index) => {
    if (index === '') return
    setForm(testPresets[index].data)
    setResult(null)
    setError('')
  }

  const predict = async () => {
    setError('')
    setResult(null)
    setLoading(true)

    const stages = [
      '🔄 Preparing your data...',
      '🧠 Running AI analysis...',
      '📊 Calculating risk factors...',
      '✨ Generating results...',
    ]
    for (const s of stages) {
      setStage(s)
      await new Promise(r => setTimeout(r, 500))
    }

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Prediction failed')
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
      setStage('')
    }
  }

  return (
    <div className="predict-page">
      <h1 className="page-title">🔬 Heart Disease Risk Predictor</h1>
      <p className="page-subtitle">Enter your clinical parameters to assess your heart disease risk</p>

      <div className="warning-banner">
        ⚠️ <strong>Disclaimer:</strong> This is NOT a medical diagnosis. Always consult a healthcare provider.
      </div>

      <div className="preset-bar">
        <label className="preset-label">⚡ Quick Fill Test Case
          <select className="preset-select" defaultValue="" onChange={e => applyPreset(e.target.value)}>
            <option value="" disabled>Select a test case...</option>
            {testPresets.map((p, i) => <option key={i} value={i}>{p.label}</option>)}
          </select>
        </label>
      </div>

      <div className="form-grid">
        {/* Left column */}
        <div>
          <h3 className="section-header">👤 Basic Information</h3>
          <label>Age (years)
            <input type="number" min={1} max={120} value={form.age} onChange={e => set('age', e.target.value)} />
          </label>
          <label>Biological Sex
            <select value={form.sex} onChange={e => set('sex', e.target.value)}>
              <option value={1}>Male</option>
              <option value={0}>Female</option>
            </select>
          </label>

          <h3 className="section-header">❤️ Heart Measurements</h3>
          <label>Resting Blood Pressure (mm Hg)
            <input type="number" min={80} max={250} value={form.trtbps} onChange={e => set('trtbps', e.target.value)} />
            <span className="help-text">Normal: &lt;120 mm Hg</span>
          </label>
          <label>Cholesterol Level (mg/dl)
            <input type="range" min={100} max={600} step={5} value={form.chol} onChange={e => set('chol', e.target.value)} />
            <span className="range-value">{form.chol} mg/dl</span>
            <span className="help-text">Desirable: &lt;200 mg/dl</span>
          </label>
          <label>Maximum Heart Rate
            <input type="range" min={60} max={220} value={form.thalachh} onChange={e => set('thalachh', e.target.value)} />
            <span className="range-value">{form.thalachh} bpm</span>
            <span className="help-text">Estimate: 220 − your age</span>
          </label>
        </div>

        {/* Right column */}
        <div>
          <h3 className="section-header">🩺 Clinical Symptoms</h3>
          <label>Chest Pain Type
            <select value={form.cp} onChange={e => set('cp', e.target.value)}>
              {cpOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </label>
          <label>Fasting Blood Sugar &gt; 120 mg/dl?
            <select value={form.fbs} onChange={e => set('fbs', e.target.value)}>
              <option value={0}>No</option>
              <option value={1}>Yes</option>
            </select>
          </label>
          <label>Exercise-Induced Angina?
            <select value={form.exng} onChange={e => set('exng', e.target.value)}>
              <option value={0}>No</option>
              <option value={1}>Yes</option>
            </select>
          </label>

          <h3 className="section-header">📊 ECG &amp; Test Results</h3>
          <label>Resting ECG Results
            <select value={form.restecg} onChange={e => set('restecg', e.target.value)}>
              {restecgOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </label>
          <label>ST Depression (Oldpeak)
            <input type="range" min={0} max={6} step={0.1} value={form.oldpeak} onChange={e => set('oldpeak', e.target.value)} />
            <span className="range-value">{form.oldpeak}</span>
          </label>
        </div>
      </div>

      {/* Extra row */}
      <h3 className="section-header">🔎 Additional Factors</h3>
      <div className="form-row-3">
        <label>Peak Exercise ST Slope
          <select value={form.slp} onChange={e => set('slp', e.target.value)}>
            {slopeOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </label>
        <label>Major Vessels (0-3)
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

      <div className="btn-center">
        <button className="btn-primary" onClick={predict} disabled={loading}>
          {loading ? stage : '🔬 Analyze My Heart Risk'}
        </button>
      </div>

      {error && <div className="alert alert-error" style={{ textAlign: 'center', marginTop: '1.5rem' }}>❌ {error}</div>}

      {result && (
        <div className={`result-card ${result.prediction === 0 ? 'result-safe' : 'result-risk'}`}>
          <div className="result-icon">{result.prediction === 0 ? '💚' : '⚠️'}</div>
          <div className="result-title">
            {result.prediction === 0 ? 'Low Risk Detected' : 'Elevated Risk Detected'}
          </div>
          <div className="result-message">
            {result.prediction === 0
              ? 'Based on the parameters provided, you appear to have a lower risk of heart disease.'
              : 'Based on the parameters provided, you may have an elevated risk of heart disease.'}
          </div>
          <p className="result-advice">
            {result.prediction === 0
              ? '✅ Continue maintaining a healthy lifestyle and get regular check-ups!'
              : '🏥 Please consult a healthcare professional for proper evaluation.'}
          </p>
          <hr className="divider" />
          <p className="result-meta">Model Confidence: {result.confidence}% · Model: {result.model_name}</p>
        </div>
      )}
    </div>
  )
}
