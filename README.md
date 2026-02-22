# ❤️ HeartGuard — Heart Attack Risk Prediction System

A full-stack machine learning application that predicts heart disease risk using clinical parameters. Built as a **Final Year Major Project**.

> **Live API** → [web-production-a175a.up.railway.app](https://web-production-a175a.up.railway.app/api/health)

---

## 🎯 Overview

HeartGuard takes 13 clinical inputs (age, cholesterol, blood pressure, etc.) and uses a **Logistic Regression** model to predict the likelihood of heart disease. The system features a modern React frontend and a Flask REST API deployed on Railway.

## 🧠 Model Training & Performance

The model was trained using `train_logistic_model.py` on the **UCI Cleveland Heart Disease** dataset (303 patients, 13 features).

### Training Pipeline

1. **Outlier Treatment** — Caps `trtbps`, `chol`, and `oldpeak` at the 90th percentile
2. **Feature Scaling** — `StandardScaler` applied via a scikit-learn `Pipeline`
3. **Model** — `LogisticRegression(max_iter=2000)`
4. **Validation** — 5-fold Stratified Cross-Validation + 80/20 train-test split

### Model Scores

| Metric | Score | What It Means |
|--------|-------|---------------|
| **CV ROC-AUC (mean)** | 0.8876 | The model correctly ranks a random positive case above a negative one ~89% of the time, averaged across 5 folds |
| **CV ROC-AUC (std)** | ±0.0628 | Low variation across folds — the model generalizes consistently |
| **Test ROC-AUC** | 0.8810 | Nearly matches CV score, confirming no overfitting |
| **Test Accuracy** | 0.8197 | Correctly classifies ~82% of unseen patients |

> **Interpretation**: An AUC of **0.88** is considered **good** for clinical screening tools. The close match between CV AUC (0.8876) and test AUC (0.8810) shows the model generalizes well without overfitting.

### Features Used (All 13)

| # | Feature | Description |
|---|---------|-------------|
| 1 | `age` | Age in years |
| 2 | `sex` | Biological sex (1 = Male, 0 = Female) |
| 3 | `cp` | Chest pain type (0–3) |
| 4 | `trtbps` | Resting blood pressure (mm Hg) |
| 5 | `chol` | Serum cholesterol (mg/dl) |
| 6 | `fbs` | Fasting blood sugar > 120 mg/dl (1 = Yes) |
| 7 | `restecg` | Resting ECG results (0–2) |
| 8 | `thalachh` | Maximum heart rate achieved |
| 9 | `exng` | Exercise-induced angina (1 = Yes) |
| 10 | `oldpeak` | ST depression induced by exercise |
| 11 | `slp` | Slope of peak exercise ST segment |
| 12 | `caa` | Number of major vessels colored by fluoroscopy (0–3) |
| 13 | `thall` | Thalassemia type |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React + Vite |
| **Backend API** | Flask + Gunicorn |
| **ML Model** | scikit-learn (Logistic Regression) |
| **Deployment** | Railway (API), Vite dev server (Frontend) |
| **Data** | Pandas, NumPy |

---

## 📂 Project Structure

```
implementation/
├── api.py                    # Flask REST API (/api/predict, /api/health)
├── train_logistic_model.py   # Model training script
├── logistic_model.joblib     # Trained model artifact
├── heart.csv                 # UCI Cleveland heart disease dataset
├── heart-attack-analysis-prediction.ipynb  # EDA & training notebook
├── Procfile                  # Railway deployment config
├── railway.json              # Railway health check & build settings
├── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages (Home, PredictRisk, Statistics, About)
│   │   ├── components/       # Reusable UI components (Navbar, Sidebar)
│   │   ├── App.jsx           # App router
│   │   └── main.jsx          # Entry point
│   ├── .env                  # API base URL (VITE_API_BASE_URL)
│   └── package.json
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Backend (Flask API)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

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

# Configure API URL
cp .env.example .env
# Edit .env → set VITE_API_BASE_URL (defaults to Railway URL)

# Start dev server
npm run dev
# → Running on http://localhost:5173
```

### 3. Test the API

```bash
# Health check
curl http://localhost:5001/api/health

# Predict (positive case)
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"age":67,"sex":1,"cp":0,"trtbps":160,"chol":286,"fbs":0,"restecg":0,"thalachh":108,"exng":1,"oldpeak":1.5,"slp":1,"caa":3,"thall":2}'
```

---

## 📊 Dataset

- **Source**: UCI Machine Learning Repository (Cleveland Database)
- **Samples**: 303 patient records
- **Features**: 13 clinical attributes
- **Target**: `output` — 1 = higher risk, 0 = lower risk

---

## 🇮🇳 India Context

- 2.8 million Indians die from heart disease every year
- 28% of all deaths in India are due to cardiovascular disease
- Indians experience heart attacks **10 years earlier** than the global average
- **80%** of heart attacks are preventable with early detection

---

## ⚠️ Disclaimer

This application is developed for **educational and research purposes** as part of an academic project. It is **NOT** a substitute for professional medical diagnosis. Always consult a healthcare provider.

---

## 📖 References

- [UCI Heart Disease Dataset](https://archive.ics.uci.edu/dataset/45/heart+disease)
- Indian Council of Medical Research (ICMR)
- Indian Heart Association
- World Health Organization (WHO)

---

**Final Year Major Project** · Heart Attack Prediction using Machine Learning · © 2025–2026
