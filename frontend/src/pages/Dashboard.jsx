import { Link } from 'react-router-dom'
import './Dashboard.css'

const stats = [
  { num: '2.8M', label: 'Deaths per year in India' },
  { num: '28%', label: 'Of all deaths in India' },
  { num: '1 in 4', label: 'Indians at risk by age 40' },
  { num: '272M', label: 'Indians with heart conditions' },
]

const risks = [
  { icon: '🧬', title: 'Genetic Predisposition', desc: 'South Asians have a higher genetic risk for heart disease, with heart attacks occurring 10 years earlier than in other populations' },
  { icon: '🍽️', title: 'Dietary Habits', desc: 'High consumption of refined carbs, trans fats, and low fiber intake contribute to rising cholesterol levels' },
  { icon: '🏙️', title: 'Urbanization & Stress', desc: 'Rapid urbanization has led to sedentary lifestyles and increased work-related stress' },
  { icon: '💉', title: 'Diabetes Epidemic', desc: 'India has 77+ million diabetics, making it the "Diabetes Capital of the World" — a major CVD risk factor' },
  { icon: '🚬', title: 'Tobacco Use', desc: 'Over 275 million Indians use tobacco, significantly increasing cardiovascular risk' },
  { icon: '🌫️', title: 'Air Pollution', desc: 'Poor air quality in major cities contributes to 25% of heart disease deaths in India' },
]

const preventions = [
  { icon: '🏃', title: 'Stay Active', desc: '30 minutes of walking, yoga, or exercise daily can reduce risk by 30-40%' },
  { icon: '🥗', title: 'Eat Healthy', desc: 'Include more vegetables, dal, whole grains; reduce oil, sugar, and processed foods' },
  { icon: '😴', title: 'Quality Sleep', desc: '7-8 hours of sleep helps your heart recover and reduces stress hormones' },
  { icon: '🧘', title: 'Manage Stress', desc: 'Practice yoga, meditation, or pranayama to control blood pressure naturally' },
  { icon: '🚭', title: 'Quit Tobacco', desc: 'Quit smoking, gutka, and pan masala — risk drops 50% within 1 year of quitting' },
  { icon: '🩺', title: 'Regular Checkups', desc: 'Get BP, blood sugar, and lipid profile checked annually after age 30' },
]

export default function Dashboard() {
  return (
    <div className="dashboard">
      {/* Hero */}
      <section className="hero">
        <span className="hero-heart">🫀</span>
        <h1 className="hero-title">HeartGuard</h1>
        <p className="hero-subtitle">AI-Powered Heart Disease Risk Assessment &amp; Awareness Platform</p>
      </section>

      <div className="warning-banner">⚠️ This tool is for educational purposes only. Always consult healthcare professionals for medical advice.</div>

      {/* Stats */}
      <h2 className="section-title">📊 Heart Disease in India</h2>
      <p className="section-subtitle">India has one of the highest burdens of cardiovascular disease in the world</p>
      <div className="grid-4">
        {stats.map(s => (
          <div className="stat-card" key={s.num}>
            <div className="stat-number">{s.num}</div>
            <div className="stat-label">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Risk Factors */}
      <h2 className="section-title">🇮🇳 Why India Is At High Risk</h2>
      <p className="section-subtitle">Unique factors contributing to heart disease in India</p>
      <div className="grid-2">
        {risks.map(r => (
          <div className="risk-card" key={r.title}>
            <div className="card-icon">{r.icon}</div>
            <div className="card-title">{r.title}</div>
            <div className="card-desc">{r.desc}</div>
          </div>
        ))}
      </div>

      {/* Prevention */}
      <h2 className="section-title">💚 Prevention Is Key</h2>
      <p className="section-subtitle">Simple lifestyle changes can dramatically reduce your risk</p>
      <div className="grid-3">
        {preventions.map(p => (
          <div className="prevention-card" key={p.title}>
            <div className="card-icon">{p.icon}</div>
            <div className="card-title">{p.title}</div>
            <div className="card-desc">{p.desc}</div>
          </div>
        ))}
      </div>

      {/* CTA */}
      <hr className="divider" />
      <section className="cta-section">
        <h2>Ready to Check Your Heart Health?</h2>
        <p>Our AI-powered tool analyzes clinical parameters to assess your risk</p>
        <Link to="/predict"><button className="btn-primary">🔬 Check Your Risk Now</button></Link>
      </section>
    </div>
  )
}
