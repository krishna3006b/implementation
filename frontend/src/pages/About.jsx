import './About.css'

const techStack = [
  '🐍 Python 3.x', '⚛️ React + Vite', '🤖 Logistic Regression',
  '📊 Pandas', '🔢 NumPy', '📈 Scikit-learn', '🌐 Flask API', '📉 Recharts',
]

export default function About() {
  return (
    <div className="about-page">
      <h1 className="page-title">ℹ️ About This Project</h1>
      <p className="page-subtitle">Heart Attack Prediction using Machine Learning</p>

      {/* Overview */}
      <h2 className="section-title">🎯 Project Overview</h2>
      <div className="info-card">
        <p>
          <strong style={{ color: '#ff8fab' }}>HeartGuard</strong> is a machine learning-based heart attack prediction system
          developed as a <strong>Final Year Major Project</strong>. The system uses clinical parameters to predict the
          likelihood of heart disease, helping in early detection and prevention.
        </p>
        <p style={{ color: '#aaa', marginTop: '1rem' }}>
          This project demonstrates the practical application of <strong style={{ color: '#ff8fab' }}>Machine Learning in Healthcare</strong> for disease prediction and awareness.
        </p>
      </div>

      {/* Objectives */}
      <h2 className="section-title">🎯 Project Objectives</h2>
      <div className="alert alert-info">
        <strong>Primary Objectives:</strong>
        <ol>
          <li>To develop a machine learning model for heart attack prediction</li>
          <li>To create an interactive web application for risk assessment</li>
          <li>To raise awareness about cardiovascular health in India</li>
          <li>To demonstrate ML application in healthcare domain</li>
        </ol>
      </div>

      {/* Tech Stack */}
      <h2 className="section-title">🛠️ Technology Stack</h2>
      <div style={{ marginBottom: '1.5rem' }}>
        {techStack.map(t => <span className="tech-badge" key={t}>{t}</span>)}
      </div>

      {/* Model Details */}
      <h2 className="section-title">🧠 Machine Learning Model</h2>
      <div className="grid-2">
        <div className="model-card">
          <h4>📊 Model Specifications</h4>
          <ul>
            <li><strong>Algorithm:</strong> Logistic Regression</li>
            <li><strong>Training Data:</strong> 303 patients</li>
            <li><strong>Features:</strong> 13 clinical parameters</li>
            <li><strong>Accuracy:</strong> ~82%</li>
            <li><strong>AUC Score:</strong> ~0.88</li>
          </ul>
        </div>
        <div className="model-card">
          <h4>🔬 Features Used</h4>
          <ul>
            <li><strong>Thalassemia</strong> — Blood disorder type</li>
            <li><strong>Major Vessels</strong> — Count via fluoroscopy</li>
            <li><strong>Chest Pain Type</strong> — Clinical symptom</li>
            <li><strong>ST Depression</strong> — ECG parameter</li>
            <li><strong>Exercise Angina</strong> — Symptom indicator</li>
            <li><strong>Cholesterol</strong> — Blood lipid level</li>
            <li><strong>Max Heart Rate</strong> — Peak rate achieved</li>
          </ul>
        </div>
      </div>

      {/* Methodology */}
      <h2 className="section-title">📋 Methodology</h2>
      <div className="info-card">
        <p style={{ color: '#ff8fab', fontWeight: 600, marginBottom: '0.8rem' }}>Development Process:</p>
        <ol style={{ color: '#fff', paddingLeft: '1.2rem', lineHeight: 2 }}>
          <li><strong>Data Collection</strong> — UCI Heart Disease Dataset (Cleveland Database)</li>
          <li><strong>Data Preprocessing</strong> — Cleaning, handling missing values</li>
          <li><strong>Exploratory Data Analysis</strong> — Understanding patterns and correlations</li>
          <li><strong>Feature Selection</strong> — Identifying most predictive features using Mutual Information</li>
          <li><strong>Model Training</strong> — Logistic Regression with cross-validation</li>
          <li><strong>Hyperparameter Tuning</strong> — Optimizing model parameters</li>
          <li><strong>Evaluation</strong> — Using accuracy, AUC score, and cross-validation</li>
          <li><strong>Deployment</strong> — React frontend + Flask API backend</li>
        </ol>
      </div>

      {/* Dataset */}
      <h2 className="section-title">📚 Dataset Information</h2>
      <div className="alert alert-info">
        <strong>Heart Disease Dataset (UCI Machine Learning Repository)</strong><br /><br />
        <strong>Source:</strong> Cleveland Database, UCI Repository<br />
        <strong>Total Samples:</strong> 303 patient records<br />
        <strong>Features:</strong> 13 clinical attributes + 1 target variable<br />
        <strong>Target Variable:</strong> Presence (1) or Absence (0) of heart disease<br />
        <strong>Attributes:</strong> Age, Sex, Chest Pain, Blood Pressure, Cholesterol, ECG, Max Heart Rate, etc.
      </div>

      {/* India Context */}
      <h2 className="section-title">🇮🇳 Relevance to India</h2>
      <div className="alert alert-success">
        <strong>Why Heart Attack Prediction Matters for India:</strong><br /><br />
        • <strong>2.8 million</strong> Indians die from heart disease every year<br />
        • Indians experience heart attacks <strong>10 years earlier</strong> than global average<br />
        • <strong>28%</strong> of all deaths in India are due to cardiovascular diseases<br />
        • <strong>80%</strong> of heart attacks are preventable with early detection<br />
        • Awareness tools like this can encourage early screening and lifestyle changes
      </div>

      {/* Disclaimer */}
      <h2 className="section-title">⚠️ Disclaimer</h2>
      <div className="alert alert-error">
        <strong>Important Notice:</strong><br /><br />
        This application is developed for <strong>educational and research purposes</strong> as part of an academic project.<br />
        • It is NOT a substitute for professional medical diagnosis<br />
        • Results should NOT be used for making medical decisions<br />
        • Always consult qualified healthcare professionals for health concerns
      </div>

      {/* References */}
      <h2 className="section-title">📖 References</h2>
      <div className="grid-2">
        <div className="info-card">
          <p style={{ color: '#ff8fab', fontWeight: 600 }}>Data Sources:</p>
          <ul style={{ paddingLeft: '1.2rem', lineHeight: 2, color: '#fff' }}>
            <li>UCI Machine Learning Repository</li>
            <li>Cleveland Heart Disease Database</li>
          </ul>
          <p style={{ color: '#ff8fab', fontWeight: 600, marginTop: '1rem' }}>Health Data:</p>
          <ul style={{ paddingLeft: '1.2rem', lineHeight: 2, color: '#fff' }}>
            <li>Indian Council of Medical Research (ICMR)</li>
            <li>World Health Organization (WHO)</li>
            <li>Indian Heart Association</li>
          </ul>
        </div>
        <div className="info-card">
          <p style={{ color: '#ff8fab', fontWeight: 600 }}>Technical References:</p>
          <ul style={{ paddingLeft: '1.2rem', lineHeight: 2, color: '#fff' }}>
            <li>Logistic Regression (Scikit-learn)</li>
            <li>React + Vite Documentation</li>
            <li>Scikit-learn Documentation</li>
          </ul>
          <p style={{ color: '#ff8fab', fontWeight: 600, marginTop: '1rem' }}>Research Papers:</p>
          <ul style={{ paddingLeft: '1.2rem', lineHeight: 2, color: '#fff' }}>
            <li>Heart Disease Prediction using ML techniques</li>
            <li>Comparative analysis of classification algorithms</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
