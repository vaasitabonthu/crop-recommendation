# 🌾 AI Crop Recommendation System

A machine learning web application that recommends the best crop for farmers based on soil nutrients and weather conditions, built using K-Nearest Neighbors (KNN) algorithm.

---

## 📁 Project Structure

```
crop-recommendation/
├── app.py                    # Streamlit web application
├── ML_project.ipynb          # Model training notebook
├── knn_crop_model.pkl        # Trained KNN model
├── Crop_recommendation.csv   # Dataset (2200 records, 22 crops)
└── README.md                 # This file
```

---

## 🚀 Features

- 🤖 **KNN AI Model** — Predicts the best crop from 22 types based on 7 input parameters
- 🌤️ **Live Weather** — Auto-fills temperature & humidity using OpenWeatherMap API
- 📊 **Confidence Ranking** — Shows top 5 crop matches with confidence percentage
- 🧠 **Why This Crop?** — Plain-language explanation of why the crop was recommended
- ⚖️ **Crop Comparison** — Side-by-side comparison of top 5 alternative crops
- 🧪 **Fertilizer Calculator** — Calculates exact bags of Urea, SSP, MOP needed per acre
- 💰 **Profit Estimator** — Estimates yield, revenue, cost and net profit
- 📅 **Crop Calendar** — Month-by-month sow → grow → harvest visual
- 📈 **Yield Trends** — 8-year historical yield trend for recommended crop
- 📱 **SMS Result** — Sends recommendation to farmer's phone via Twilio
- 🎤 **Voice Input** — Browser-based microphone input (Chrome)
- 🌐 **3 Languages** — English, తెలుగు (Telugu), हिंदी (Hindi)

---

## 🧠 Machine Learning

| Detail | Value |
|--------|-------|
| Algorithm | K-Nearest Neighbors (KNN) |
| Dataset | Crop Recommendation Dataset |
| Records | 2200 rows |
| Features | N, P, K, Temperature, Humidity, pH, Rainfall |
| Target | Crop Label (22 crops) |
| Train/Test Split | 80% / 20% |

### Input Features

| Feature | Description | Unit |
|---------|-------------|------|
| N | Nitrogen content in soil | kg/ha |
| P | Phosphorus content in soil | kg/ha |
| K | Potassium content in soil | kg/ha |
| Temperature | Average temperature | °C |
| Humidity | Relative humidity | % |
| pH | Soil pH value | 0–14 |
| Rainfall | Annual rainfall | mm |

### Crops Supported

Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee

---

## ⚙️ Installation & Setup

### 1. Install dependencies
```bash
pip install streamlit pandas numpy scikit-learn joblib requests
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🔑 API Keys (Optional)

The app works without API keys — these just unlock extra features.

### Weather Auto-fill (Free)
1. Sign up at [openweathermap.org](https://openweathermap.org/api)
2. In `app.py`, replace:
```python
OWM_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
```

### SMS via Twilio (Free tier available)
1. Sign up at [twilio.com](https://twilio.com)
2. In `app.py`, replace:
```python
TWILIO_SID   = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH  = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM  = "+1XXXXXXXXXX"
```

---

## 📊 How It Works

```
Farmer enters soil values (N, P, K, pH)
           +
    Weather data (Temp, Humidity, Rainfall)
                  ↓
         KNN Model (k=5 neighbors)
                  ↓
    Finds 5 most similar rows in training data
                  ↓
    Most common crop among neighbors = Recommendation
                  ↓
    App shows: Crop + Tips + Profit + Fertilizer + Calendar
```

---

## 🌱 Dataset

- **Source:** [Kaggle — Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- **Records:** 2200
- **Crops:** 22
- **License:** Open for educational use

---

## 📞 Farmer Helpline

**Kisan Call Centre: 1800-180-1551** (Free, 24×7, in your local language)

---

*Built as a Machine Learning project to help farmers make better crop decisions using AI.*
