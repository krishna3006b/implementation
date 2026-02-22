# ❤️ HeartGuard — AI-Powered Heart Health Platform

> A full-stack AI health platform that predicts heart disease risk, provides personalized AI coaching, gamified lifestyle tracking, and voice-first daily logging. Built as a **Final Year Major Project**.

> **Live Frontend** → [implementation-nu.vercel.app](https://implementation-nu.vercel.app)
> **Live Backend API** → [web-production-a175a.up.railway.app](https://web-production-a175a.up.railway.app/api/health)

---

## 🎯 What is HeartGuard?

HeartGuard goes **far beyond** a simple ML prediction tool. It is a **habit-forming health platform** that combines clinical risk assessment with daily lifestyle management powered by AI.

### Core Capabilities

| Module | Description |
|--------|-------------|
| 🔬 **Risk Prediction** | ML model (Logistic Regression, AUC 0.88) predicts heart disease risk from 13 clinical inputs |
| 🤖 **AI Health Coach** | Groq-powered LLM provides personalized briefings, chat, and weekly insights |
| 📋 **Protocol Generator** | AI generates 4-week personalized health protocols after risk prediction |
| 🎮 **Gamification Engine** | Daily quests, streaks, XP system, badges, and a living Habit Spark micro-pet |
| 🎙️ **Voice-First Logging** | Speak your daily update — AI parses it into structured goal data automatically |
| 📆 **GitHub Heatmap** | 60-day contribution graph showing your health consistency at a glance |
| 🧠 **AI Personas** | Choose between 4 coaching styles: Supportive, Tough Love, Zen Master, or Data Scientist |

---

## 🖼️ Platform Pages

| Page | What It Does |
|------|-------------|
| **Home** | Heart disease awareness, India-specific statistics, call-to-action |
| **Predict Risk** | 13-input clinical form → ML prediction → AI Protocol Generator |
| **Lifestyle** | Daily tracking dashboard with goals, mood, energy, AI coach, quests, heatmap |
| **Statistics** | Healthcare data visualizations and cardiovascular statistics |
| **About** | Methodology, ML model details, academic references |

---

## 🧠 ML Model & Training

Trained using `train_logistic_model.py` on the **UCI Cleveland Heart Disease** dataset (303 patients, 13 features).

### Training Pipeline

1. **Outlier Treatment** — Caps `trtbps`, `chol`, and `oldpeak` at the 90th percentile
2. **Feature Scaling** — `StandardScaler` applied via a scikit-learn `Pipeline`
3. **Model** — `LogisticRegression(max_iter=2000)`
4. **Validation** — 5-fold Stratified Cross-Validation + 80/20 train-test split

### Model Performance

| Metric | Score |
|--------|-------|
| **CV ROC-AUC (mean)** | 0.8876 |
| **CV ROC-AUC (std)** | ±0.0628 |
| **Test ROC-AUC** | 0.8810 |
| **Test Accuracy** | 81.97% |

> An AUC of **0.88** is considered **good** for clinical screening. The close match between CV and test AUC confirms no overfitting.

### Clinical Features Used (All 13)

| # | Feature | Description |
|---|---------|-------------|
| 1 | `age` | Age in years |
| 2 | `sex` | Biological sex (1 = Male, 0 = Female) |
| 3 | `cp` | Chest pain type (0–3) |
| 4 | `trtbps` | Resting blood pressure (mm Hg) |
| 5 | `chol` | Serum cholesterol (mg/dl) |
| 6 | `fbs` | Fasting blood sugar > 120 mg/dl |
| 7 | `restecg` | Resting ECG results (0–2) |
| 8 | `thalachh` | Maximum heart rate achieved |
| 9 | `exng` | Exercise-induced angina |
| 10 | `oldpeak` | ST depression induced by exercise |
| 11 | `slp` | Slope of peak exercise ST segment |
| 12 | `caa` | Major vessels colored by fluoroscopy (0–3) |
| 13 | `thall` | Thalassemia type |

---

## 🤖 AI Features (Groq LLM Integration)

HeartGuard uses **Groq's ultra-fast LLM inference** for all AI features:

### AI Health Coach
- **Daily Briefing**: Personalized health tips based on the user's tracking data, risk profile, goals, and streaks
- **Real-time Chat**: Users can ask health questions and get contextual answers
- **Weekly Insights**: AI analyzes 7-day tracking patterns and provides trend analysis

### Protocol Generator
After receiving their risk prediction, users can generate a **personalized 4-week health protocol**. The AI creates structured diet, exercise, and supplement recommendations that are automatically injected into the user's goal list.

### Voice-First Logging
Users tap a microphone button and speak naturally:
> *"I drank 6 glasses of water, walked 8000 steps, and I'm feeling good today"*

The AI parses this into structured data (mood, energy, goal completions, values) using Groq's JSON mode and auto-fills the tracking form.

### AI Personas
Four distinct coaching personalities that alter the AI's communication style:

| Persona | Style |
|---------|-------|
| 🤗 **Supportive Coach** | Warm, encouraging, celebrates small wins |
| 🔥 **Tough Love** | No-nonsense drill sergeant, pushes accountability |
| 🧘 **Zen Master** | Calm, mindful, focused on balance and self-compassion |
| 🔬 **Data Scientist** | Numbers-driven, trend analysis, evidence-based |

---

## 🎮 Gamification System

### Daily Quests
The AI generates one unique, time-sensitive quest per day based on the user's health goals. Completing it awards XP and triggers a confetti celebration.

### Habit Spark (Micro-Pet)
A living, breathing CSS orb that reflects the user's streak:
- **Sleeping** (grey, slow pulse) — Streak 0
- **Awakening** (yellow glow) — Streak 1–2
- **Glowing** (cyan, with particles) — Streak 3–6
- **Blazing** (pink, intense aura) — Streak 7+

### Streaks & Badges
- Current/best streak tracking with motivational messages
- Auto-awarded badges for milestones: 7-day, 14-day, 30-day streaks

### GitHub-Style Heatmap
A 60-day contribution graph visualizing daily health tracking consistency, with 4 intensity levels based on goal completion percentage.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite |
| **UI Design** | Glassmorphism, CSS keyframe animations, dark theme |
| **Backend API** | Flask + Gunicorn |
| **Database** | MongoDB (via PyMongo) |
| **Authentication** | JWT (PyJWT) — Register/Login/Protected routes |
| **AI/LLM** | Groq API (llama-3.3-70b-versatile) |
| **ML Model** | scikit-learn (Logistic Regression) |
| **Voice Input** | Browser SpeechRecognition API |
| **Deployment** | Railway (Backend), Vercel (Frontend) |
| **Data** | Pandas, NumPy, Joblib |

---

## 📂 Project Structure

```
implementation/
├── api.py                    # Flask app factory, ML prediction endpoint
├── auth_routes.py            # JWT auth: register, login, /me
├── goals_routes.py           # CRUD for user health goals
├── tracker_routes.py         # Daily log tracking, streaks, heatmap data
├── ai_routes.py              # AI coach, chat, quests, protocol, voice, personas
├── train_logistic_model.py   # Model training script
├── logistic_model.joblib     # Trained model artifact
├── heart.csv                 # UCI Cleveland heart disease dataset
├── hear-disease-ml-notebook.ipynb  # EDA & training notebook
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment config
├── railway.json              # Railway build settings
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Home page with awareness content
│   │   │   ├── PredictRisk.jsx     # Risk prediction wizard + Protocol Generator
│   │   │   ├── Lifestyle.jsx       # Main dashboard: tracking, AI, gamification
│   │   │   ├── Statistics.jsx      # Healthcare data visualizations
│   │   │   ├── About.jsx           # Methodology & references
│   │   │   └── Login.jsx           # Authentication page
│   │   ├── components/
│   │   │   └── PageWrapper.jsx     # Animated page transitions
│   │   ├── context/
│   │   │   └── AuthContext.jsx     # JWT authentication context
│   │   ├── App.jsx                 # Router & layout
│   │   ├── App.css                 # Global styles & design system
│   │   └── index.css               # CSS reset & variables
│   ├── .env                        # API base URL config
│   └── package.json
│
└── README.md
```

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### 1. Backend (Flask API)

```bash
# Clone and enter the project
git clone https://github.com/krishna3006b/implementation.git
cd implementation

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY=your_groq_api_key
export MONGO_URI=mongodb://localhost:27017/heartguard
export JWT_SECRET=your_secret_key

# (Optional) Re-train the model
python3 train_logistic_model.py --data heart.csv --target output --risk-label 1

# Start the API server
python3 api.py
# → Running on http://localhost:5001
```

### 2. Frontend (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → Running on http://localhost:5173
```

### 3. Test the API

```bash
# Health check
curl http://localhost:5001/api/health

# Predict heart disease risk
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"age":67,"sex":1,"cp":0,"trtbps":160,"chol":286,"fbs":0,"restecg":0,"thalachh":108,"exng":1,"oldpeak":1.5,"slp":1,"caa":3,"thall":2}'
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login → returns JWT |
| GET | `/api/auth/me` | Get current user profile |

### Prediction
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/predict` | Predict heart disease risk |
| GET | `/api/health` | API health check |

### Lifestyle Tracking
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/goals` | Get user goals |
| POST | `/api/goals` | Update user goals |
| GET | `/api/tracker?days=60` | Get daily logs (heatmap data) |
| POST | `/api/tracker/today` | Save today's tracking progress |
| GET | `/api/tracker/streak` | Get streak statistics |

### AI Features
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/ai/coach` | Generate AI daily briefing |
| POST | `/api/ai/chat` | Chat with AI health coach |
| POST | `/api/ai/insights` | Generate weekly insights |
| POST | `/api/ai/quest` | Get/generate daily quest |
| POST | `/api/ai/quest/complete` | Complete daily quest |
| POST | `/api/ai/protocol` | Generate health protocol |
| POST | `/api/ai/parse-log` | Parse voice transcript → structured data |
| GET | `/api/ai/persona` | Get available AI personas |
| POST | `/api/ai/persona` | Set preferred AI persona |

---

## 📊 Dataset

- **Source**: UCI Machine Learning Repository (Cleveland Database)
- **Samples**: 303 patient records
- **Features**: 13 clinical attributes
- **Target**: `output` — 1 = higher risk, 0 = lower risk

---

## 🇮🇳 India Context

- **2.8 million** Indians die from heart disease every year
- **28%** of all deaths in India are due to cardiovascular disease
- Indians experience heart attacks **10 years earlier** than the global average
- **80%** of heart attacks are preventable with early detection

---

## 🏗️ Development Phases

| Phase | Focus | Key Deliverables |
|-------|-------|-----------------|
| **A** | Core UI & Design | Glassmorphism theme, dark mode, responsive layout, page transitions |
| **B** | Dashboard & Tracking | Lifestyle dashboard, goal tracking, mood/energy logging, calendar |
| **C** | AI Integration | AI Coach briefing, chat, weekly insights, badge system |
| **D** | Ultra-Gamification | Daily Quests, Protocol Generator, confetti rewards, XP system |
| **E** | Elite Platform | GitHub Heatmap, Habit Spark micro-pet, Voice Logging, AI Personas |

---

## ⚠️ Disclaimer

This application is developed for **educational and research purposes** as part of an academic project. It is **NOT** a substitute for professional medical diagnosis. Always consult a healthcare provider.

---

## 📖 References

- [UCI Heart Disease Dataset](https://archive.ics.uci.edu/dataset/45/heart+disease)
- [Groq API Documentation](https://console.groq.com/docs)
- Indian Council of Medical Research (ICMR)
- Indian Heart Association
- World Health Organization (WHO)
- Web Speech API (MDN)

---

**Final Year Major Project** · Heart Attack Prediction & AI Health Platform · © 2025–2026
