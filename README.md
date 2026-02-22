# HeartGuard - Heart Attack Prediction System

A machine learning-based heart attack prediction system developed as a **Final Year Major Project**.

## 🎯 Project Overview

HeartGuard uses machine learning to predict the likelihood of heart disease based on clinical parameters. The system helps in early detection and raises awareness about cardiovascular health in India.

## 🚀 Features

- **AI-Powered Risk Prediction** - Logistic Regression classifier with validated ROC-AUC
- **Interactive Dashboard** - India-focused heart disease statistics
- **User-Friendly Interface** - Modern, responsive web application
- **Real-time Analysis** - Instant risk assessment with visual feedback

## 🛠️ Technology Stack

- **Python 3.x** - Core programming language
- **Streamlit** - Web application framework
- **Logistic Regression** - Machine learning algorithm
- **Pandas & NumPy** - Data processing
- **Scikit-learn** - Model evaluation

## 📊 Dataset

- **Source**: UCI Machine Learning Repository (Cleveland Database)
- **Samples**: 303 patient records
- **Features**: 13 clinical attributes
- **Target**: Presence or absence of heart disease

## 🔬 ML Model Details

| Specification | Value |
|---------------|-------|
| Algorithm | Logistic Regression |
| Features Used | 7 clinical parameters |
| Accuracy | ~85% |
| AUC Score | ~0.87 |

### Key Features Used:
- Thalassemia type
- Major vessels count (fluoroscopy)
- Chest pain type
- ST depression (Oldpeak)
- Exercise-induced angina
- Cholesterol level
- Maximum heart rate

## 📂 Project Structure

```
implementation/
├── Dashboard.py              # Main homepage
├── pages/
│   ├── 1_🔬_Predict_Risk.py  # Prediction page
│   ├── 2_📊_Statistics.py    # India statistics
│   └── 3_ℹ️_About.py         # Project information
├── logistic_model.joblib     # Trained Logistic Regression model
├── train_logistic_model.py   # Model training script
├── requirements.txt          # Python dependencies
├── heart-attack-analysis-prediction.ipynb  # Model training notebook
└── README.md
```

## ⚙️ Installation & Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train logistic model**
   ```bash
   python3 train_logistic_model.py --data /path/to/heart.csv --target output --risk-label 1
   ```

4. **Run the application**
   ```bash
   streamlit run Dashboard.py
   ```

5. **Open in browser**
   ```
   http://localhost:8501
   ```

## 🇮🇳 India Context

- 2.8 million Indians die from heart disease every year
- 28% of all deaths in India are due to CVD
- Indians experience heart attacks 10 years earlier than global average
- 80% of heart attacks are preventable with early detection

## ⚠️ Disclaimer

This application is developed for **educational and research purposes** as part of an academic project. It is NOT a substitute for professional medical diagnosis.

## 📖 References

- UCI Machine Learning Repository
- Indian Council of Medical Research (ICMR)
- Indian Heart Association
- World Health Organization (WHO)

---

**Final Year Major Project** | Heart Attack Prediction using Machine Learning | © 2024-2025
