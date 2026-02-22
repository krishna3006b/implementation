import { Link } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import './Statistics.css'

const ageData = [
  { group: '25-34', pct: 5 },
  { group: '35-44', pct: 12 },
  { group: '45-54', pct: 22 },
  { group: '55-64', pct: 38 },
  { group: '65-74', pct: 52 },
  { group: '75+', pct: 65 },
]

const riskData = [
  { factor: 'Hypertension', pct: 35 },
  { factor: 'Diabetes', pct: 28 },
  { factor: 'Tobacco Use', pct: 25 },
  { factor: 'Obesity', pct: 20 },
  { factor: 'Air Pollution', pct: 18 },
  { factor: 'Physical Inactivity', pct: 15 },
  { factor: 'Unhealthy Diet', pct: 12 },
]

const states = [
  { name: 'Punjab', rate: '15.6%', note: 'Highest CVD prevalence' },
  { name: 'Kerala', rate: '14.8%', note: 'High urban CVD rate' },
  { name: 'Tamil Nadu', rate: '13.5%', note: 'Rising CVD cases' },
]

export default function Statistics() {
  return (
    <div className="stats-page">
      <h1 className="page-title">📊 Heart Disease Statistics — India</h1>
      <p className="page-subtitle">Understanding the cardiovascular disease burden in India</p>

      {/* Overview */}
      <h2 className="section-title">🇮🇳 India Overview</h2>
      <div className="grid-4">
        {[ ['2.8M','Deaths per year in India'], ['28%','Of all deaths in India'], ['272M','Indians with CVD conditions'], ['54.5M','Living with heart disease'] ]
          .map(([n,l]) => <div className="stat-card" key={n}><div className="stat-number">{n}</div><div className="stat-label">{l}</div></div>)}
      </div>

      <hr className="divider" />

      {/* Age Chart */}
      <h2 className="section-title">📈 CVD Prevalence by Age in India</h2>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={ageData}>
            <XAxis dataKey="group" stroke="#aaa" />
            <YAxis stroke="#aaa" unit="%" />
            <Tooltip contentStyle={{ background: '#1a1a2e', border: '1px solid #ff8fab', borderRadius: 10, color: '#fff' }} />
            <Bar dataKey="pct" name="Prevalence %" radius={[8,8,0,0]}>
              {ageData.map((_, i) => <Cell key={i} fill="#ff6b9d" />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="chart-caption">Prevalence of cardiovascular disease by age group in India (Source: ICMR)</p>
      </div>

      <hr className="divider" />

      {/* State-wise */}
      <h2 className="section-title">🗺️ State-wise CVD Burden</h2>
      <div className="grid-3">
        {states.map(s => (
          <div className="stat-card" key={s.name}>
            <h4 style={{ color: '#ff8fab' }}>{s.name}</h4>
            <div className="stat-number">{s.rate}</div>
            <div className="stat-label">{s.note}</div>
          </div>
        ))}
      </div>

      <hr className="divider" />

      {/* Gender */}
      <h2 className="section-title">👥 Gender Statistics — India</h2>
      <div className="grid-2">
        <div className="gender-card male">
          <h3>👨 Men in India</h3>
          <div className="stat-number" style={{ color: '#6bb3ff' }}>17.8%</div>
          <div className="stat-label">Of Indian men affected by CVD</div>
          <ul>
            <li>Average age of first heart attack: <strong>50 years</strong></li>
            <li>10 years earlier than global average</li>
            <li>Higher risk due to stress &amp; smoking</li>
          </ul>
        </div>
        <div className="gender-card female">
          <h3>👩 Women in India</h3>
          <div className="stat-number" style={{ color: '#ff8fab' }}>13.2%</div>
          <div className="stat-label">Of Indian women affected by CVD</div>
          <ul>
            <li>Risk increases sharply after menopause</li>
            <li>Often underdiagnosed due to different symptoms</li>
            <li>PCOS increases risk in younger women</li>
          </ul>
        </div>
      </div>

      <hr className="divider" />

      {/* Risk Factor Chart */}
      <h2 className="section-title">⚠️ Major Risk Factors in India</h2>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={riskData} layout="vertical">
            <XAxis type="number" stroke="#aaa" unit="%" />
            <YAxis dataKey="factor" type="category" stroke="#aaa" width={140} />
            <Tooltip contentStyle={{ background: '#1a1a2e', border: '1px solid #ff8fab', borderRadius: 10, color: '#fff' }} />
            <Bar dataKey="pct" name="Contribution %" radius={[0,8,8,0]}>
              {riskData.map((_, i) => <Cell key={i} fill="#ff6b9d" />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <p className="chart-caption">Contribution of risk factors to CVD in India (Source: Indian Heart Association)</p>
      </div>

      <hr className="divider" />

      {/* India vs Global */}
      <h2 className="section-title">🌍 India vs Global Comparison</h2>
      <div className="grid-2">
        <div className="stat-card">
          <h4 style={{ color: '#ff8fab' }}>🇮🇳 India</h4>
          <div className="stat-number">2.8M</div>
          <div className="stat-label">CVD deaths per year</div>
          <p style={{ color: '#aaa', marginTop: '1rem', fontSize: '0.9rem' }}>Average age of first heart attack: <strong style={{ color: '#ff8fab' }}>50 years</strong></p>
        </div>
        <div className="stat-card">
          <h4 style={{ color: '#ff8fab' }}>🌍 Global</h4>
          <div className="stat-number">17.9M</div>
          <div className="stat-label">CVD deaths per year</div>
          <p style={{ color: '#aaa', marginTop: '1rem', fontSize: '0.9rem' }}>Average age of first heart attack: <strong style={{ color: '#ff8fab' }}>60 years</strong></p>
        </div>
      </div>

      <hr className="divider" />

      {/* Key Takeaways */}
      <h2 className="section-title">💡 Key Takeaways for India</h2>
      <div className="alert alert-success">
        <strong>Important Facts for Indians:</strong><br />
        ✅ Indians are at higher genetic risk — heart attacks occur 10 years earlier<br />
        ✅ Up to <strong>80%</strong> of heart attacks are preventable with lifestyle changes<br />
        ✅ Regular screening after age 30 is crucial<br />
        ✅ Traditional practices like yoga can significantly reduce risk
      </div>

      <hr className="divider" />
      <div style={{ textAlign: 'center' }}>
        <Link to="/predict"><button className="btn-primary">🔬 Check Your Risk Now</button></Link>
      </div>
    </div>
  )
}
