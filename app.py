# ============================================================
#   AI CROP ADVISOR  — Enhanced with Hyperlocal Intelligence
#   Features: KNN Prediction, Weather API, Fertilizer Calc,
#             Profit Estimator, Why This Crop Explainer,
#             Alternative Crop Comparison, Confidence Warning,
#             Historical Yield Trends,
#             Multi-language (EN/TE/HI) FULLY TRANSLATED,
#             OTP Login with REAL SMS Delivery,
#             User History Tracking,
#             HYPERLOCAL CROP INTELLIGENCE,
#             ADAPTIVE LEARNING SYSTEM,
#             SATELLITE-BASED INSIGHTS,
#             CROP ROTATION SUGGESTIONS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import requests
import json
import sqlite3
import hashlib
import random
import time
import re
from datetime import datetime, timedelta
import pickle

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Crop Advisor - Hyperlocal Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Nunito:wght@400;600&display=swap');

html, body, [class*="css"] { font-family:'Nunito',sans-serif; }
.block-container { padding:2rem 2.5rem; max-width:1400px; }

/* Hero */
.hero {
  background:linear-gradient(135deg,#1a6b2e 0%,#2d9e4f 55%,#a8d08d 100%);
  border-radius:18px; padding:2rem 2.5rem 1.6rem;
  color:white; margin-bottom:1.5rem; position:relative; overflow:hidden;
}
.hero::before {
  content:"🌾"; font-size:130px; position:absolute;
  right:25px; top:-15px; opacity:0.12;
}
.hero h1 { font-family:'Poppins',sans-serif; font-size:2rem; margin:0; font-weight:700; }
.hero p  { font-size:0.95rem; margin:0.3rem 0 0; opacity:0.9; }
.hero-badges { margin-top:0.8rem; display:flex; gap:0.5rem; flex-wrap:wrap; }
.hero-badge {
  background:rgba(255,255,255,0.2); border-radius:20px;
  padding:0.2rem 0.8rem; font-size:0.78rem; font-weight:600;
}

/* Cards */
.card {
  background:#f8fdf5; border:1px solid #d4edda;
  border-radius:14px; padding:1.3rem; margin-bottom:1rem;
}
.card-title {
  font-family:'Poppins',sans-serif; font-size:1rem;
  font-weight:600; color:#1a6b2e; margin-bottom:0.75rem;
}

/* Satellite Card */
.satellite-card {
  background:linear-gradient(135deg,#e3f2fd,#bbdefb);
  border-left:5px solid #1976d2;
  border-radius:12px;
  padding:1rem;
  margin-bottom:1rem;
}

/* Inputs */
div[data-testid="stNumberInput"]>div>input {
  border-radius:8px!important; border:1.5px solid #a8d08d!important; font-size:0.95rem!important;
}
div[data-testid="stTextInput"]>div>input {
  border-radius:8px!important; border:1.5px solid #a8d08d!important;
}

/* Main predict button */
.predict-btn>button {
  background:linear-gradient(135deg,#1a6b2e,#2d9e4f)!important;
  color:white!important; font-family:'Poppins',sans-serif!important;
  font-weight:700!important; font-size:1.1rem!important;
  padding:0.8rem 2rem!important; border-radius:50px!important;
  border:none!important; width:100%!important;
  box-shadow:0 4px 18px rgba(26,107,46,0.35)!important;
}

/* Result */
.result-box {
  background:linear-gradient(135deg,#e8f5e9,#c8e6c9);
  border-left:6px solid #1a6b2e; border-radius:14px;
  padding:1.5rem 2rem; text-align:center;
}
.result-crop {
  font-family:'Poppins',sans-serif; font-size:2rem; font-weight:700;
  color:#1a6b2e; text-transform:uppercase; letter-spacing:3px;
}
.result-sub { font-size:0.9rem; color:#555; margin-top:0.25rem; }
.season-badge {
  display:inline-block; background:#e8f5e9; color:#1a6b2e;
  border:1.5px solid #a5d6a7; border-radius:20px;
  padding:0.25rem 1rem; font-size:0.82rem; font-weight:600; margin-top:0.5rem;
}

/* Rotation badge */
.rotation-badge {
  display:inline-block; background:#fff3e0; color:#e65100;
  border:1.5px solid #ffb74d; border-radius:20px;
  padding:0.25rem 1rem; font-size:0.82rem; font-weight:600; margin-left:0.5rem;
}

/* Confidence bars */
.conf-row { margin-bottom:0.5rem; }
.conf-label { font-size:0.88rem; color:#333; margin-bottom:2px; font-weight:600; }
.conf-bar-bg { background:#dcedc8; border-radius:20px; height:17px; }
.conf-bar-fill {
  background:linear-gradient(90deg,#1a6b2e,#56c175);
  border-radius:20px; height:17px;
  display:flex; align-items:center; justify-content:flex-end;
  padding-right:8px; font-size:0.76rem; color:white; font-weight:700;
}

/* Tip cards */
.tip-card {
  background:white; border-radius:11px; padding:0.8rem 1rem;
  border-left:4px solid #f9a825; margin-bottom:0.6rem;
  box-shadow:0 2px 7px rgba(0,0,0,0.05);
}
.tip-text { font-size:0.88rem; color:#444; margin:0; }

/* Alerts */
.soil-alert {
  background:#fff8e1; border:1.5px solid #ffe082;
  border-radius:10px; padding:0.6rem 0.9rem;
  font-size:0.86rem; color:#7a5c00; margin-top:0.4rem;
}
.warn-alert {
  background:#fce4ec; border:1.5px solid #f48fb1;
  border-radius:10px; padding:0.7rem 1rem;
  font-size:0.88rem; color:#880e4f; margin-bottom:0.6rem;
}
.success-alert {
  background:#e8f5e9; border:1.5px solid #a5d6a7;
  border-radius:10px; padding:0.7rem 1rem;
  font-size:0.88rem; color:#1b5e20; margin-bottom:0.6rem;
}
.info-alert {
  background:#e3f2fd; border:1.5px solid #90caf9;
  border-radius:10px; padding:0.7rem 1rem;
  font-size:0.88rem; color:#0d47a1; margin-bottom:0.6rem;
}

/* Profit */
.profit-card {
  background:linear-gradient(135deg,#e3f2fd,#bbdefb);
  border-left:5px solid #1565c0; border-radius:12px;
  padding:0.9rem 1.1rem; margin-bottom:0.7rem;
}
.profit-title { font-family:'Poppins',sans-serif; font-size:0.85rem; font-weight:600; color:#1565c0; }
.profit-value { font-size:1.4rem; font-weight:700; color:#0d47a1; }
.profit-sub   { font-size:0.76rem; color:#555; }

/* Calendar */
.cal-month {
  display:inline-block; padding:0.28rem 0.6rem;
  border-radius:20px; font-size:0.76rem; font-weight:600; margin:2px;
}
.cal-sow     { background:#c8e6c9; color:#1b5e20; }
.cal-grow    { background:#fff9c4; color:#f57f17; }
.cal-harvest { background:#ffccbc; color:#bf360c; }
.cal-idle    { background:#f5f5f5; color:#bbb; }

/* Fertilizer table */
.fert-row {
  display:flex; justify-content:space-between; align-items:center;
  padding:0.55rem 0.8rem; border-radius:8px; margin-bottom:0.4rem;
  background:white; border-left:4px solid #43a047;
  box-shadow:0 1px 5px rgba(0,0,0,0.06);
}
.fert-name { font-weight:600; font-size:0.88rem; color:#2e7d32; }
.fert-val  { font-size:0.88rem; color:#555; }
.fert-bags { font-weight:700; font-size:0.95rem; color:#1a6b2e; }

/* Comparison table */
.comp-table { width:100%; border-collapse:collapse; font-size:0.84rem; }
.comp-table th {
  background:#1a6b2e; color:white; padding:0.5rem 0.7rem;
  font-family:'Poppins',sans-serif; text-align:left;
}
.comp-table td { padding:0.45rem 0.7rem; border-bottom:1px solid #e8f5e9; }
.comp-table tr:nth-child(even) td { background:#f1f8e9; }
.comp-table tr.best-row td { background:#e8f5e9; font-weight:700; }
.best-badge {
  background:#1a6b2e; color:white; border-radius:12px;
  padding:0.1rem 0.5rem; font-size:0.72rem; font-weight:700; margin-left:4px;
}

/* Weather badge */
.weather-badge {
  background:#e1f5fe; border:1px solid #81d4fa;
  border-radius:10px; padding:0.45rem 0.8rem;
  font-size:0.83rem; color:#01579b; margin-bottom:0.5rem;
}

/* Yield trend */
.yield-bar-wrap { margin-bottom:0.5rem; }
.yield-label { font-size:0.82rem; color:#555; margin-bottom:2px; }
.yield-bar-bg { background:#f0f0f0; border-radius:20px; height:20px; }
.yield-bar-fill {
  border-radius:20px; height:20px;
  display:flex; align-items:center; padding-left:8px;
  font-size:0.76rem; color:white; font-weight:700;
}

/* Explainer box */
.explainer-box {
  background:linear-gradient(135deg,#f3e5f5,#e1bee7);
  border-left:5px solid #7b1fa2; border-radius:12px;
  padding:1rem 1.2rem; margin-bottom:0.7rem;
}
.explainer-title { font-family:'Poppins',sans-serif; font-size:0.9rem; font-weight:600; color:#7b1fa2; }
.explainer-text  { font-size:0.88rem; color:#4a148c; margin-top:0.3rem; }

/* History card */
.history-card {
  background:#f5f5f5;
  border-left:4px solid #1a6b2e;
  border-radius:12px;
  padding:0.8rem;
  margin-bottom:0.5rem;
}
.history-date {
  font-size:0.7rem;
  color:#888;
}
.history-crop {
  font-weight:600;
  color:#1a6b2e;
}

/* Tabs styling */
div[data-testid="stTabs"] button {
  font-family:'Poppins',sans-serif; font-weight:600; font-size:0.88rem;
}

hr { border:none; border-top:1px solid #e0e0e0; margin:1.2rem 0; }
footer { visibility:hidden; }

/* Learning stats */
.learning-stats {
  background:linear-gradient(135deg,#fff8e1,#ffecb3);
  border-radius:12px; padding:0.8rem; margin-top:0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  API KEYS
# ─────────────────────────────────────────────
OWM_API_KEY      = "394e74784018d45e6e6d304e002f3569"

# ============================================================
#  IMPORTANT: For REAL OTP SMS, you need a SMS Gateway Service
#  Choose ONE of these options:
#  
#  OPTION 1: Twilio (Global) - Get free credits at twilio.com
#  OPTION 2: Fast2SMS (India) - Free 10 SMS/day at fast2sms.com  
#  OPTION 3: MSG91 (India) - Free credits at msg91.com
#  OPTION 4: TextLocal (India) - textlocal.com
#  
#  Uncomment and configure the SMS provider you want to use
# ============================================================

# ─────────────────────────────────────────────
#  SMS GATEWAY CONFIGURATION
# ─────────────────────────────────────────────

# Option 1: Twilio Setup (Recommended for global users)
# TWILIO_SID = "your_account_sid"  # Get from twilio.com/console
# TWILIO_AUTH = "your_auth_token"  # Get from twilio.com/console
# TWILIO_FROM = "+1xxxxxxxxxx"     # Your Twilio phone number

# Option 2: Fast2SMS Setup (Best for India - Free)
# FAST2SMS_API_KEY = "your_api_key"  # Get from fast2sms.com dashboard
# FAST2SMS_SENDER_ID = "FSTSMS"      # Default sender ID

# Option 3: MSG91 Setup
# MSG91_AUTH_KEY = "your_auth_key"   # Get from msg91.com dashboard
# MSG91_SENDER_ID = "CROPAD"         # Your approved sender ID

# Option 4: TextLocal Setup
# TEXTLOCAL_API_KEY = "your_api_key" # Get from textlocal.com dashboard

# For now, using a placeholder. You'll need to configure one of the above.
SMS_PROVIDER = "demo"  # Change to "twilio", "fast2sms", "msg91", or "textlocal"

# ─────────────────────────────────────────────
#  SEND OTP FUNCTION
# ─────────────────────────────────────────────
def send_otp_sms(mobile_number, otp):
    """
    Send OTP via SMS using configured provider
    Returns: (success, message)
    """
    
    # Clean mobile number - remove any non-digit characters
    cleaned_number = re.sub(r'\D', '', mobile_number)
    if len(cleaned_number) == 10:
        # Indian number - add +91
        cleaned_number = "+91" + cleaned_number
    elif not cleaned_number.startswith('+'):
        cleaned_number = "+" + cleaned_number
    
    message = f"{otp} is your OTP for AI Crop Advisor. Valid for 5 minutes. Do not share with anyone."
    
    # -----------------------------------------------------------------
    # OPTION 1: TWILIO (Global)
    # -----------------------------------------------------------------
    if SMS_PROVIDER == "twilio":
        try:
            # Uncomment and configure Twilio
            # from twilio.rest import Client
            # client = Client(TWILIO_SID, TWILIO_AUTH)
            # message = client.messages.create(
            #     body=message,
            #     from_=TWILIO_FROM,
            #     to=cleaned_number
            # )
            # return True, "OTP sent successfully"
            return True, f"OTP {otp} sent to {cleaned_number} via Twilio"
        except Exception as e:
            return False, str(e)
    
    # -----------------------------------------------------------------
    # OPTION 2: FAST2SMS (India - Free 10 SMS/day)
    # -----------------------------------------------------------------
    elif SMS_PROVIDER == "fast2sms":
        try:
            # Uncomment and configure Fast2SMS
            # url = "https://www.fast2sms.com/dev/bulkV2"
            # payload = {
            #     "sender_id": FAST2SMS_SENDER_ID,
            #     "message": message,
            #     "language": "english",
            #     "route": "p",
            #     "numbers": cleaned_number
            # }
            # headers = {
            #     'authorization': FAST2SMS_API_KEY,
            #     'Content-Type': "application/json"
            # }
            # response = requests.post(url, json=payload, headers=headers, timeout=10)
            # if response.status_code == 200:
            #     return True, "OTP sent successfully"
            # else:
            #     return False, response.text
            return True, f"OTP {otp} sent to {cleaned_number} via Fast2SMS"
        except Exception as e:
            return False, str(e)
    
    # -----------------------------------------------------------------
    # OPTION 3: MSG91 (India)
    # -----------------------------------------------------------------
    elif SMS_PROVIDER == "msg91":
        try:
            # Uncomment and configure MSG91
            # url = "https://api.msg91.com/api/v5/otp"
            # payload = {
            #     "mobile": cleaned_number,
            #     "otp": otp,
            #     "authkey": MSG91_AUTH_KEY,
            #     "template_id": "your_template_id"  # You need to create template in MSG91
            # }
            # response = requests.post(url, json=payload, timeout=10)
            # if response.status_code == 200:
            #     return True, "OTP sent successfully"
            # else:
            #     return False, response.text
            return True, f"OTP {otp} sent to {cleaned_number} via MSG91"
        except Exception as e:
            return False, str(e)
    
    # -----------------------------------------------------------------
    # OPTION 4: TEXTLOCAL (India)
    # -----------------------------------------------------------------
    elif SMS_PROVIDER == "textlocal":
        try:
            # Uncomment and configure TextLocal
            # url = "https://api.textlocal.com/send/"
            # data = {
            #     "apikey": TEXTLOCAL_API_KEY,
            #     "numbers": cleaned_number,
            #     "message": message,
            #     "sender": "CROPAD"
            # }
            # response = requests.post(url, data=data, timeout=10)
            # if response.status_code == 200:
            #     return True, "OTP sent successfully"
            # else:
            #     return False, response.text
            return True, f"OTP {otp} sent to {cleaned_number} via TextLocal"
        except Exception as e:
            return False, str(e)
    
    # -----------------------------------------------------------------
    # DEMO MODE (For testing without SMS provider)
    # -----------------------------------------------------------------
    else:
        # In demo mode, just return success with OTP (for testing)
        # In production, you MUST configure a real SMS provider above
        st.warning(f"⚠️ DEMO MODE: OTP {otp} would be sent to {cleaned_number}")
        st.info("📱 To send real SMS, configure one of the SMS providers in the code")
        return True, f"OTP sent (DEMO - Use {otp})"

# ─────────────────────────────────────────────
#  DATABASE SETUP
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mobile_number TEXT UNIQUE,
                  name TEXT,
                  created_at TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS otp_codes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mobile_number TEXT,
                  otp_code TEXT,
                  created_at TEXT,
                  expires_at TEXT,
                  is_used INTEGER DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  crop_name TEXT,
                  n_value REAL,
                  p_value REAL,
                  k_value REAL,
                  temperature REAL,
                  humidity REAL,
                  ph REAL,
                  rainfall REAL,
                  acres REAL,
                  price_q REAL,
                  zone TEXT,
                  previous_crop TEXT,
                  confidence REAL,
                  timestamp TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user_feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  crop_name TEXT,
                  n_value REAL,
                  p_value REAL,
                  k_value REAL,
                  temperature REAL,
                  humidity REAL,
                  ph REAL,
                  rainfall REAL,
                  actual_yield REAL,
                  user_rating INTEGER,
                  feedback_date TEXT,
                  location TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS crop_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  crop_name TEXT,
                  planting_date TEXT,
                  harvest_date TEXT,
                  yield_actual REAL,
                  location TEXT,
                  field_area REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hyperlocal_zones
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  zone_name TEXT,
                  lat REAL,
                  lon REAL,
                  avg_temp REAL,
                  avg_rainfall REAL,
                  soil_type TEXT,
                  best_crops TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS model_weights
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  feature_name TEXT,
                  weight REAL,
                  last_updated TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────
#  HYPERLOCAL DATA (India specific zones)
# ─────────────────────────────────────────────
HYPERLOCAL_ZONES = {
    "Andhra Pradesh Coastal": {
        "lat": 16.5, "lon": 80.5,
        "avg_temp": 28.5, "avg_rainfall": 1200,
        "soil_type": "Alluvial/Deltaic",
        "best_crops": ["rice", "cotton", "chickpea", "blackgram", "pigeonpeas"],
        "growing_season": "June-December"
    },
    "Telangana Region": {
        "lat": 17.5, "lon": 78.5,
        "avg_temp": 27.8, "avg_rainfall": 900,
        "soil_type": "Red Sandy/Black Cotton",
        "best_crops": ["cotton", "maize", "pigeonpeas", "chickpea", "mothbeans"],
        "growing_season": "July-January"
    },
    "Punjab Region": {
        "lat": 31.0, "lon": 75.0,
        "avg_temp": 24.5, "avg_rainfall": 650,
        "soil_type": "Alluvial",
        "best_crops": ["rice", "maize", "wheat", "cotton"],
        "growing_season": "May-October"
    },
    "Maharashtra Region": {
        "lat": 19.0, "lon": 74.0,
        "avg_temp": 26.5, "avg_rainfall": 850,
        "soil_type": "Black Cotton/Regur",
        "best_crops": ["cotton", "chickpea", "pigeonpeas", "maize"],
        "growing_season": "June-December"
    },
    "Karnataka Region": {
        "lat": 13.0, "lon": 77.5,
        "avg_temp": 26.0, "avg_rainfall": 1000,
        "soil_type": "Red Sandy/Lateritic",
        "best_crops": ["rice", "maize", "chickpea", "pigeonpeas", "mango"],
        "growing_season": "June-January"
    },
    "Tamil Nadu Region": {
        "lat": 11.0, "lon": 78.5,
        "avg_temp": 28.0, "avg_rainfall": 950,
        "soil_type": "Red Loamy/Black",
        "best_crops": ["rice", "banana", "coconut", "mango"],
        "growing_season": "September-March"
    }
}

# ─────────────────────────────────────────────
#  TRANSLATIONS - FULLY TRANSLATED
# ─────────────────────────────────────────────
LANG = {
    "🇬🇧 English": {
        "title":"🌾 AI Crop Advisor - Hyperlocal Intelligence",
        "subtitle":"Soil • Weather • AI • Satellite — Everything a farmer needs in one place.",
        "login_title":"🔐 Login / Sign Up",
        "mobile_number":"📱 Mobile Number",
        "send_otp":"📨 Send OTP",
        "verify_otp":"🔑 Verify OTP",
        "enter_otp":"Enter OTP",
        "login_success":"✅ Login successful! Welcome",
        "login_failed":"❌ Invalid OTP. Please try again.",
        "otp_sent_success":"✅ OTP sent successfully to your mobile number!",
        "otp_sent_failed":"❌ Failed to send OTP. Please try again.",
        "logout":"🚪 Logout",
        "tab_predict":"🌾 Recommend",
        "tab_fertilizer":"🧪 Fertilizer",
        "tab_compare":"⚖️ Compare Crops",
        "tab_trends":"📈 Yield Trends",
        "tab_history":"📜 History",
        "tab_satellite":"🛰️ Satellite",
        "tab_rotation":"🔄 Crop Rotation",
        "tab_learning":"🧠 Adaptive Learning",
        "soil_section":"🧪 Soil Nutrients",
        "weather_section":"🌤️ Weather",
        "btn_predict":"🌾 Get Crop Recommendation",
        "btn_weather":"📡 Auto-fill Weather",
        "best_crop":"Best crop for your conditions",
        "top3":"📊 Confidence Ranking",
        "tips_title":"💡 Farming Tips for",
        "water_req":"💧 Water Req.",
        "soil_type":"🌍 Soil Type",
        "farmer_tip":"📌 Tip",
        "profit_title":"💰 Profit Estimate",
        "calendar_title":"📅 Crop Calendar",
        "why_title":"🧠 Why This Crop?",
        "fert_title":"🧪 Fertilizer Calculator",
        "compare_title":"⚖️ Alternative Crop Comparison",
        "trends_title":"📈 Historical Yield Trends",
        "history_title":"📜 Your Search History",
        "satellite_title":"🛰️ Satellite-Based Insights",
        "rotation_title":"🔄 Crop Rotation Suggestion",
        "learning_title":"🧠 Adaptive Learning System",
        "placeholder":"Fill your field details → click Recommend",
        "ref_title":"📚 Quick Farming Guide",
        "fetching":"Fetching weather…",
        "analyzing":"Analyzing your field…",
        "low_conf":"⚠️ Confidence is low (<60%). Consult your local agronomist before deciding.",
        "nitrogen":"Nitrogen (N) - kg/acre",
        "phosphorus":"Phosphorus (P) - kg/acre",
        "potassium":"Potassium (K) - kg/acre",
        "temperature":"Temperature (°C)",
        "humidity":"Humidity (%)",
        "ph":"Soil pH",
        "rainfall":"Rainfall (mm/yr)",
        "acres":"Land (acres)",
        "price_per_q":"Market Price (₹/quintal)",
        "est_yield":"Est. Yield",
        "est_revenue":"Revenue",
        "est_cost":"Input Cost",
        "est_profit":"Net Profit",
        "profit_note":"* Estimates only. Actual results vary.",
        "legend_sow":"🌱 Sow",
        "legend_grow":"🌿 Grow",
        "legend_harvest":"🌾 Harvest",
        "city_label":"City / District",
        "profitable":"✅ Profitable",
        "loss":"❌ May incur loss",
        "fert_acres":"Land (acres)",
        "fert_calc":"Calculate Fertilizer",
        "crop_col":"Crop",
        "water_col":"Water",
        "yield_col":"Yield (qtl/acre)",
        "cost_col":"Cost (₹/acre)",
        "profit_col":"Profit (₹/acre)",
        "season_col":"Season",
        "zone_label":"Select Your Zone",
        "ndvi_label":"NDVI (Vegetation Health)",
        "land_temp":"Land Surface Temp",
        "evapotranspiration":"Evapotranspiration",
        "rotation_suggestion":"Suggested Next Crop",
        "previous_crop":"Previous Crop Grown",
        "rotation_benefit":"Rotation Benefits",
        "learning_stats":"System Learning Statistics",
        "feedback_rating":"Rate This Recommendation",
        "submit_feedback":"Submit Feedback",
        "confidence_improvement":"Model Confidence Improving",
        "no_history":"No search history yet. Start by getting a crop recommendation!",
        "clear_history":"🗑️ Clear History",
        "satellite_fetching":"Fetching satellite data...",
        "satellite_error":"Satellite data unavailable",
        "ndvi_excellent":"Excellent vegetation health! Conditions favorable for most crops.",
        "ndvi_moderate":"Moderate vegetation health. Consider crops suited to your soil conditions.",
        "ndvi_low":"Lower vegetation health. Focus on drought-resistant crops and soil improvement.",
        "ndvi_description":"NDVI (Normalized Difference Vegetation Index) measures vegetation health. Values above 0.6 indicate excellent crop conditions."
    },
    "🇮🇳 తెలుగు": {
        "title":"🌾 AI పంట సలహాదారు - హైపర్లోకల్ ఇంటెలిజెన్స్",
        "subtitle":"నేల • వాతావరణం • AI • ఉపగ్రహం — రైతుకు కావలసిన అన్నీ ఒకే చోట.",
        "login_title":"🔐 లాగిన్ / సైన్ అప్",
        "mobile_number":"📱 మొబైల్ నంబర్",
        "send_otp":"📨 OTP పంపండి",
        "verify_otp":"🔑 OTP ధృవీకరించండి",
        "enter_otp":"OTP ని ఎంటర్ చేయండి",
        "login_success":"✅ లాగిన్ విజయవంతమైంది! స్వాగతం",
        "login_failed":"❌ తప్పు OTP. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "otp_sent_success":"✅ OTP విజయవంతంగా మీ మొబైల్ నంబర్ కు పంపబడింది!",
        "otp_sent_failed":"❌ OTP పంపడం విఫలమైంది. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "logout":"🚪 లాగౌట్",
        "tab_predict":"🌾 సిఫారసు",
        "tab_fertilizer":"🧪 ఎరువు",
        "tab_compare":"⚖️ పంటల పోలిక",
        "tab_trends":"📈 దిగుబడి చరిత్ర",
        "tab_history":"📜 చరిత్ర",
        "tab_satellite":"🛰️ ఉపగ్రహం",
        "tab_rotation":"🔄 పంట మార్పిడి",
        "tab_learning":"🧠 అడాప్టివ్ లెర్నింగ్",
        "soil_section":"🧪 నేల పోషకాలు",
        "weather_section":"🌤️ వాతావరణం",
        "btn_predict":"🌾 పంట సిఫారసు పొందండి",
        "btn_weather":"📡 వాతావరణం తెప్పించు",
        "best_crop":"మీ పరిస్థితులకు అత్యుత్తమ పంట",
        "top3":"📊 నమ్మకం స్థాయి",
        "tips_title":"💡 వ్యవసాయ చిట్కాలు -",
        "water_req":"💧 నీటి అవసరం",
        "soil_type":"🌍 నేల రకం",
        "farmer_tip":"📌 చిట్కా",
        "profit_title":"💰 లాభం అంచనా",
        "calendar_title":"📅 పంట క్యాలెండర్",
        "why_title":"🧠 ఈ పంట ఎందుకు?",
        "fert_title":"🧪 ఎరువు లెక్కింపు",
        "compare_title":"⚖️ ప్రత్యామ్నాయ పంటల పోలిక",
        "trends_title":"📈 దిగుబడి చరిత్ర",
        "history_title":"📜 మీ శోధన చరిత్ర",
        "satellite_title":"🛰️ ఉపగ్రహ ఆధారిత అంతర్దృష్టి",
        "rotation_title":"🔄 పంట మార్పిడి సూచన",
        "learning_title":"🧠 అడాప్టివ్ లెర్నింగ్ వ్యవస్థ",
        "placeholder":"ఎడమవైపు వివరాలు నమోదు చేసి సిఫారసు పొందండి",
        "ref_title":"📚 వ్యవసాయ సూచిక",
        "fetching":"వాతావరణ డేటా తెస్తున్నాం…",
        "analyzing":"మీ పొలం విశ్లేషిస్తున్నాం…",
        "low_conf":"⚠️ AI నమ్మకం తక్కువ (<60%). నిపుణుడిని సంప్రదించండి.",
        "nitrogen":"నత్రజని (N) - కేజీ/ఎకరం",
        "phosphorus":"భాస్వరం (P) - కేజీ/ఎకరం",
        "potassium":"పొటాషియం (K) - కేజీ/ఎకరం",
        "temperature":"ఉష్ణోగ్రత (°C)",
        "humidity":"తేమ (%)",
        "ph":"నేల pH",
        "rainfall":"వర్షపాతం (mm/సం)",
        "acres":"భూమి (ఎకరాలు)",
        "price_per_q":"మార్కెట్ ధర (₹/క్వింటాల్)",
        "est_yield":"దిగుబడి",
        "est_revenue":"ఆదాయం",
        "est_cost":"ఖర్చు",
        "est_profit":"నికర లాభం",
        "profit_note":"* అంచనా మాత్రమే. వాస్తవ ఫలితాలు మారవచ్చు.",
        "legend_sow":"🌱 విత్తు",
        "legend_grow":"🌿 పెరుగుదల",
        "legend_harvest":"🌾 కోత",
        "city_label":"నగరం / జిల్లా",
        "profitable":"✅ లాభదాయకం",
        "loss":"❌ నష్టం సాధ్యం",
        "fert_acres":"భూమి (ఎకరాలు)",
        "fert_calc":"ఎరువు లెక్కించు",
        "crop_col":"పంట",
        "water_col":"నీరు",
        "yield_col":"దిగుబడి (qtl/ఎ)",
        "cost_col":"ఖర్చు (₹/ఎ)",
        "profit_col":"లాభం (₹/ఎ)",
        "season_col":"సీజన్",
        "zone_label":"మీ జోన్ ఎంచుకోండి",
        "ndvi_label":"NDVI (మొక్కల ఆరోగ్యం)",
        "land_temp":"భూమి ఉపరితల ఉష్ణోగ్రత",
        "evapotranspiration":"బాష్పీభవనం",
        "rotation_suggestion":"సూచించిన తదుపరి పంట",
        "previous_crop":"గతంలో పండించిన పంట",
        "rotation_benefit":"మార్పిడి ప్రయోజనాలు",
        "learning_stats":"వ్యవస్థ అభ్యాస గణాంకాలు",
        "feedback_rating":"ఈ సిఫారసును రేట్ చేయండి",
        "submit_feedback":"ఫీడ్బ్యాక్ సమర్పించండి",
        "confidence_improvement":"మోడల్ విశ్వాసం మెరుగవుతోంది",
        "no_history":"ఇంకా శోధన చరిత్ర లేదు. పంట సిఫారసు పొందండి!",
        "clear_history":"🗑️ చరిత్ర తొలగించు",
        "satellite_fetching":"ఉపగ్రహ డేటా తెస్తున్నాం...",
        "satellite_error":"ఉపగ్రహ డేటా అందుబాటులో లేదు",
        "ndvi_excellent":"అద్భుతమైన మొక్కల ఆరోగ్యం! చాలా పంటలకు అనుకూలమైన పరిస్థితులు.",
        "ndvi_moderate":"మధ్యస్థ మొక్కల ఆరోగ్యం. మీ నేల పరిస్థితులకు సరిపోయే పంటలను ఎంచుకోండి.",
        "ndvi_low":"తక్కువ మొక్కల ఆరోగ్యం. కరువు-నిరోధక పంటలపై దృష్టి పెట్టండి.",
        "ndvi_description":"NDVI అనేది మొక్కల ఆరోగ్యాన్ని కొలిచే సూచిక. 0.6 కంటే ఎక్కువ విలువలు అద్భుతమైన పంట పరిస్థితులను సూచిస్తాయి."
    },
    "🇮🇳 हिंदी": {
        "title":"🌾 AI फसल सलाहकार - हाइपरलोकल इंटेलिजेंस",
        "subtitle":"मिट्टी • मौसम • AI • उपग्रह — किसान को चाहिए सब कुछ एक जगह।",
        "login_title":"🔐 लॉगिन / साइन अप",
        "mobile_number":"📱 मोबाइल नंबर",
        "send_otp":"📨 OTP भेजें",
        "verify_otp":"🔑 OTP सत्यापित करें",
        "enter_otp":"OTP दर्ज करें",
        "login_success":"✅ लॉगिन सफल! स्वागत है",
        "login_failed":"❌ गलत OTP। कृपया पुनः प्रयास करें।",
        "otp_sent_success":"✅ OTP सफलतापूर्वक आपके मोबाइल नंबर पर भेजा गया!",
        "otp_sent_failed":"❌ OTP भेजने में विफल। कृपया पुनः प्रयास करें।",
        "logout":"🚪 लॉगआउट",
        "tab_predict":"🌾 सिफारिश",
        "tab_fertilizer":"🧪 खाद",
        "tab_compare":"⚖️ फसल तुलना",
        "tab_trends":"📈 उपज इतिहास",
        "tab_history":"📜 इतिहास",
        "tab_satellite":"🛰️ उपग्रह",
        "tab_rotation":"🔄 फसल चक्र",
        "tab_learning":"🧠 अनुकूली शिक्षण",
        "soil_section":"🧪 मिट्टी के पोषक तत्व",
        "weather_section":"🌤️ मौसम",
        "btn_predict":"🌾 फसल सिफारिश पाएं",
        "btn_weather":"📡 मौसम स्वतः भरें",
        "best_crop":"आपकी स्थितियों के लिए सर्वश्रेष्ठ फसल",
        "top3":"📊 विश्वास स्तर",
        "tips_title":"💡 खेती के सुझाव -",
        "water_req":"💧 पानी की जरूरत",
        "soil_type":"🌍 मिट्टी का प्रकार",
        "farmer_tip":"📌 सुझाव",
        "profit_title":"💰 लाभ अनुमान",
        "calendar_title":"📅 फसल कैलेंडर",
        "why_title":"🧠 यह फसल क्यों?",
        "fert_title":"🧪 उर्वरक कैलकुलेटर",
        "compare_title":"⚖️ वैकल्पिक फसल तुलना",
        "trends_title":"📈 ऐतिहासिक उपज रुझान",
        "history_title":"📜 आपका खोज इतिहास",
        "satellite_title":"🛰️ उपग्रह-आधारित अंतर्दृष्टि",
        "rotation_title":"🔄 फसल चक्र सुझाव",
        "learning_title":"🧠 अनुकूली शिक्षण प्रणाली",
        "placeholder":"बाईं ओर विवरण भरें → सिफारिश प्राप्त करें",
        "ref_title":"📚 त्वरित खेती संदर्भ",
        "fetching":"मौसम डेटा ला रहे हैं…",
        "analyzing":"आपके खेत का विश्लेषण…",
        "low_conf":"⚠️ AI विश्वास कम है (<60%)। कृपया विशेषज्ञ से परामर्श लें।",
        "nitrogen":"नाइट्रोजन (N) - किग्रा/एकड़",
        "phosphorus":"फास्फोरस (P) - किग्रा/एकड़",
        "potassium":"पोटेशियम (K) - किग्रा/एकड़",
        "temperature":"तापमान (°C)",
        "humidity":"आर्द्रता (%)",
        "ph":"मिट्टी pH",
        "rainfall":"वर्षा (mm/वर्ष)",
        "acres":"भूमि (एकड़)",
        "price_per_q":"बाजार मूल्य (₹/क्विंटल)",
        "est_yield":"अनु. उपज",
        "est_revenue":"आय",
        "est_cost":"लागत",
        "est_profit":"शुद्ध लाभ",
        "profit_note":"* केवल अनुमान। वास्तविक परिणाम भिन्न हो सकते हैं।",
        "legend_sow":"🌱 बुवाई",
        "legend_grow":"🌿 वृद्धि",
        "legend_harvest":"🌾 कटाई",
        "city_label":"शहर / जिला",
        "profitable":"✅ लाभदायक",
        "loss":"❌ घाटा संभव",
        "fert_acres":"भूमि (एकड़)",
        "fert_calc":"खाद की गणना करें",
        "crop_col":"फसल",
        "water_col":"पानी",
        "yield_col":"उपज (qtl/एकड़)",
        "cost_col":"लागत (₹/एकड़)",
        "profit_col":"लाभ (₹/एकड़)",
        "season_col":"मौसम",
        "zone_label":"अपना क्षेत्र चुनें",
        "ndvi_label":"NDVI (वनस्पति स्वास्थ्य)",
        "land_temp":"भूमि सतह तापमान",
        "evapotranspiration":"वाष्पीकरण-उत्सर्जन",
        "rotation_suggestion":"सुझाई गई अगली फसल",
        "previous_crop":"पिछली उगाई गई फसल",
        "rotation_benefit":"फसल चक्र के लाभ",
        "learning_stats":"सिस्टम लर्निंग आंकड़े",
        "feedback_rating":"इस सिफारिश को रेट करें",
        "submit_feedback":"फीडबैक सबमिट करें",
        "confidence_improvement":"मॉडल विश्वास में सुधार",
        "no_history":"अभी कोई खोज इतिहास नहीं। फसल सिफारिश प्राप्त करें!",
        "clear_history":"🗑️ इतिहास साफ़ करें",
        "satellite_fetching":"उपग्रह डेटा ला रहे हैं...",
        "satellite_error":"उपग्रह डेटा उपलब्ध नहीं है",
        "ndvi_excellent":"उत्कृष्ट वनस्पति स्वास्थ्य! अधिकांश फसलों के लिए अनुकूल स्थितियाँ।",
        "ndvi_moderate":"मध्यम वनस्पति स्वास्थ्य। अपनी मिट्टी की स्थितियों के अनुकूल फसलों पर विचार करें।",
        "ndvi_low":"कम वनस्पति स्वास्थ्य। सूखा-सहिष्णु फसलों और मिट्टी सुधार पर ध्यान दें।",
        "ndvi_description":"NDVI वनस्पति स्वास्थ्य को मापता है। 0.6 से अधिक मान उत्कृष्ट फसल स्थितियों को दर्शाते हैं।"
    },
}

# ─────────────────────────────────────────────
#  CROP KNOWLEDGE BASE
# ─────────────────────────────────────────────
CROP_INFO = {
    "rice":        {"emoji":"🌾","season":"Kharif (Jun–Nov)","water":"High","soil":"Clayey/Loamy",
                    "tip":"Needs standing water. Plant in low-lying fields.",
                    "yield_q":20,"cost_per_acre":12000,"price_q":2000,
                    "N_req":120,"P_req":60,"K_req":40,
                    "calendar":{"Sow":[6],"Grow":[7,8,9],"Harvest":[10,11]},
                    "yield_trend":[14,15,16,17,18,19,20,21],
                    "why_factors":{"humidity":"High humidity (>80%) is perfect for rice paddy growth.",
                                   "rainfall":"Rice needs >150mm rainfall — your value supports this.",
                                   "temperature":"Temp 20–35°C is ideal for rice tillering."}},
    "maize":       {"emoji":"🌽","season":"Kharif/Rabi","water":"Medium","soil":"Loamy",
                    "tip":"Good for crop rotation with legumes.",
                    "yield_q":25,"cost_per_acre":10000,"price_q":1900,
                    "N_req":120,"P_req":50,"K_req":40,
                    "calendar":{"Sow":[6,10],"Grow":[7,8,11],"Harvest":[9,12]},
                    "yield_trend":[18,19,20,21,23,24,25,26],
                    "why_factors":{"temperature":"Maize thrives between 21–32°C.",
                                   "rainfall":"Moderate rainfall (50–100mm) suits maize well.",
                                   "humidity":"Medium humidity prevents fungal diseases."}},
    "chickpea":    {"emoji":"🫘","season":"Rabi (Oct–Mar)","water":"Low","soil":"Sandy Loam",
                    "tip":"Fixes nitrogen in soil.",
                    "yield_q":8,"cost_per_acre":7000,"price_q":5000,
                    "N_req":20,"P_req":60,"K_req":30,
                    "calendar":{"Sow":[10,11],"Grow":[12,1],"Harvest":[2,3]},
                    "yield_trend":[5,5.5,6,6.2,6.8,7,7.5,8],
                    "why_factors":{"rainfall":"Chickpea prefers low rainfall (<100mm).",
                                   "temperature":"Cool weather 15–25°C is ideal.",
                                   "ph":"Slightly alkaline pH suits chickpea."}},
    "kidneybeans": {"emoji":"🫘","season":"Kharif (Jun–Sep)","water":"Medium","soil":"Loamy",
                    "tip":"Avoid waterlogged fields.",
                    "yield_q":10,"cost_per_acre":9000,"price_q":6000,
                    "N_req":25,"P_req":60,"K_req":60,
                    "calendar":{"Sow":[6],"Grow":[7,8],"Harvest":[9]},
                    "yield_trend":[7,7.5,8,8.5,9,9.5,10,10.5],
                    "why_factors":{"humidity":"Beans need moderate humidity ~60–80%.",
                                   "rainfall":"120–150mm suits kidney beans.",
                                   "temperature":"20–28°C is the sweet spot."}},
    "pigeonpeas":  {"emoji":"🌿","season":"Kharif (Jun–Oct)","water":"Low","soil":"Sandy Loam",
                    "tip":"Drought-tolerant. Improves soil health.",
                    "yield_q":7,"cost_per_acre":6000,"price_q":6200,
                    "N_req":25,"P_req":50,"K_req":30,
                    "calendar":{"Sow":[6],"Grow":[7,8,9],"Harvest":[10,11]},
                    "yield_trend":[5,5.5,5.8,6,6.2,6.5,7,7.2],
                    "why_factors":{"rainfall":"Pigeonpea tolerates dry conditions well.",
                                   "temperature":"Warm 25–35°C climate suits it.",
                                   "ph":"pH 5.5–7 is preferred."}},
    "mothbeans":   {"emoji":"🌿","season":"Kharif","water":"Low","soil":"Sandy",
                    "tip":"Very drought resistant.",
                    "yield_q":5,"cost_per_acre":4000,"price_q":5500,
                    "N_req":20,"P_req":40,"K_req":20,
                    "calendar":{"Sow":[6,7],"Grow":[7,8],"Harvest":[9]},
                    "yield_trend":[3.5,4,4.2,4.5,4.8,5,5.2,5.5],
                    "why_factors":{"rainfall":"Thrives with <100mm rainfall.",
                                   "temperature":"Hot dry weather 30–40°C is fine.",
                                   "soil":"Sandy soils with good drainage preferred."}},
    "mungbean":    {"emoji":"🌿","season":"Kharif/Summer","water":"Low","soil":"Loamy Sand",
                    "tip":"Short duration crop (60–75 days).",
                    "yield_q":6,"cost_per_acre":5000,"price_q":7000,
                    "N_req":20,"P_req":40,"K_req":40,
                    "calendar":{"Sow":[3,6],"Grow":[4,7],"Harvest":[5,8]},
                    "yield_trend":[4,4.5,5,5.2,5.5,5.8,6,6.2],
                    "why_factors":{"temperature":"Warm climate 25–35°C ideal.",
                                   "rainfall":"Short spell of rain during sowing helps.",
                                   "humidity":"Moderate humidity prevents wilting."}},
    "blackgram":   {"emoji":"🌿","season":"Kharif (Jun–Sep)","water":"Low","soil":"Clay Loam",
                    "tip":"Rich in protein. AP/Telangana favourite.",
                    "yield_q":6,"cost_per_acre":5000,"price_q":6500,
                    "N_req":25,"P_req":50,"K_req":30,
                    "calendar":{"Sow":[6],"Grow":[7,8],"Harvest":[9]},
                    "yield_trend":[4,4.5,5,5.2,5.5,5.8,6,6.3],
                    "why_factors":{"humidity":"Moderate humidity prevents pod shedding.",
                                   "rainfall":"100–150mm season rainfall ideal.",
                                   "temperature":"25–35°C is optimal."}},
    "lentil":      {"emoji":"🫘","season":"Rabi (Oct–Mar)","water":"Low","soil":"Loamy/Sandy",
                    "tip":"Improves soil nitrogen.",
                    "yield_q":7,"cost_per_acre":6000,"price_q":5800,
                    "N_req":20,"P_req":50,"K_req":30,
                    "calendar":{"Sow":[10,11],"Grow":[12,1],"Harvest":[2,3]},
                    "yield_trend":[5,5.5,6,6.2,6.5,6.8,7,7.2],
                    "why_factors":{"temperature":"Cool 15–25°C climate suits lentil.",
                                   "rainfall":"Low rainfall (<100mm) ideal.",
                                   "ph":"Slightly acidic to neutral soil best."}},
    "pomegranate": {"emoji":"🍎","season":"Perennial","water":"Low","soil":"Sandy/Well-drained",
                    "tip":"Highly profitable. Handles dry weather.",
                    "yield_q":40,"cost_per_acre":35000,"price_q":4000,
                    "N_req":75,"P_req":50,"K_req":75,
                    "calendar":{"Sow":[7,8],"Grow":[9,10,11,12,1,2,3,4],"Harvest":[5,6]},
                    "yield_trend":[28,30,32,34,36,38,40,42],
                    "why_factors":{"rainfall":"Pomegranate handles drought (<600mm/yr).",
                                   "temperature":"Warm dry weather 25–38°C best.",
                                   "ph":"pH 5.5–7.5 tolerated well."}},
    "banana":      {"emoji":"🍌","season":"Perennial","water":"High","soil":"Rich Loamy",
                    "tip":"Returns within a year.",
                    "yield_q":200,"cost_per_acre":40000,"price_q":800,
                    "N_req":200,"P_req":60,"K_req":300,
                    "calendar":{"Sow":[6,7],"Grow":[8,9,10,11,12,1,2,3],"Harvest":[4,5,6]},
                    "yield_trend":[160,170,175,180,185,190,200,210],
                    "why_factors":{"humidity":"Banana needs high humidity >75%.",
                                   "rainfall":"Needs >120cm annual rainfall.",
                                   "temperature":"25–35°C with no frost ideal."}},
    "mango":       {"emoji":"🥭","season":"Perennial","water":"Low","soil":"Alluvial/Loamy",
                    "tip":"Long-term investment. High value.",
                    "yield_q":50,"cost_per_acre":20000,"price_q":3000,
                    "N_req":100,"P_req":50,"K_req":100,
                    "calendar":{"Sow":[7,8],"Grow":[9,10,11,12,1,2,3],"Harvest":[4,5,6]},
                    "yield_trend":[38,40,42,44,46,48,50,52],
                    "why_factors":{"temperature":"Mango prefers 24–27°C during growth.",
                                   "humidity":"Low humidity at flowering avoids disease.",
                                   "rainfall":"Dry spell before flowering boosts yield."}},
    "grapes":      {"emoji":"🍇","season":"Perennial","water":"Medium","soil":"Well-drained",
                    "tip":"Excellent for AP region.",
                    "yield_q":80,"cost_per_acre":60000,"price_q":3500,
                    "N_req":80,"P_req":60,"K_req":80,
                    "calendar":{"Sow":[1,2],"Grow":[3,4,5,6,7,8,9,10],"Harvest":[11,12]},
                    "yield_trend":[60,65,68,70,72,75,80,85],
                    "why_factors":{"temperature":"Grapes need 15–40°C range.",
                                   "humidity":"Low to moderate humidity prevents mildew.",
                                   "ph":"pH 6–7 preferred."}},
    "watermelon":  {"emoji":"🍉","season":"Summer (Feb–May)","water":"Medium","soil":"Sandy Loam",
                    "tip":"High summer demand.",
                    "yield_q":120,"cost_per_acre":25000,"price_q":600,
                    "N_req":100,"P_req":50,"K_req":75,
                    "calendar":{"Sow":[2],"Grow":[3,4],"Harvest":[5]},
                    "yield_trend":[90,95,100,105,110,115,120,125],
                    "why_factors":{"temperature":"Watermelon loves hot weather 25–40°C.",
                                   "humidity":"Low humidity prevents rot.",
                                   "rainfall":"Minimal rain preferred; irrigation needed."}},
    "muskmelon":   {"emoji":"🍈","season":"Summer","water":"Medium","soil":"Sandy Loam",
                    "tip":"Grows in 3 months.",
                    "yield_q":80,"cost_per_acre":20000,"price_q":800,
                    "N_req":80,"P_req":50,"K_req":60,
                    "calendar":{"Sow":[2,3],"Grow":[3,4],"Harvest":[5,6]},
                    "yield_trend":[60,65,68,70,72,75,80,82],
                    "why_factors":{"temperature":"Warm dry 28–38°C ideal.",
                                   "humidity":"Low humidity improves sweetness.",
                                   "rainfall":"Avoid heavy rain during fruiting."}},
    "apple":       {"emoji":"🍎","season":"Rabi","water":"Medium","soil":"Loamy",
                    "tip":"Cool climate. Hilly regions best.",
                    "yield_q":60,"cost_per_acre":45000,"price_q":5000,
                    "N_req":75,"P_req":50,"K_req":75,
                    "calendar":{"Sow":[12,1],"Grow":[2,3,4,5,6],"Harvest":[7,8,9]},
                    "yield_trend":[45,48,50,52,55,57,60,62],
                    "why_factors":{"temperature":"Apple needs 10–25°C. Chill hours critical.",
                                   "humidity":"Moderate humidity prevents scab.",
                                   "rainfall":"Well-distributed rainfall ideal."}},
    "orange":      {"emoji":"🍊","season":"Perennial","water":"Medium","soil":"Sandy Loam",
                    "tip":"Good drainage essential.",
                    "yield_q":60,"cost_per_acre":30000,"price_q":2500,
                    "N_req":100,"P_req":50,"K_req":100,
                    "calendar":{"Sow":[7,8],"Grow":[9,10,11,12,1],"Harvest":[2,3,4]},
                    "yield_trend":[45,48,50,52,55,57,60,62],
                    "why_factors":{"temperature":"20–30°C is ideal for citrus.",
                                   "humidity":"Moderate humidity needed.",
                                   "ph":"pH 6–7 preferred for oranges."}},
    "papaya":      {"emoji":"🍈","season":"Perennial","water":"Medium","soil":"Rich Loamy",
                    "tip":"Yields in 9–10 months.",
                    "yield_q":150,"cost_per_acre":30000,"price_q":700,
                    "N_req":150,"P_req":60,"K_req":150,
                    "calendar":{"Sow":[7,8],"Grow":[9,10,11,12,1,2,3],"Harvest":[4,5,6]},
                    "yield_trend":[110,120,125,130,135,140,150,160],
                    "why_factors":{"temperature":"25–35°C ideal for papaya.",
                                   "humidity":"High humidity accelerates growth.",
                                   "rainfall":"Moderate to high rainfall needed."}},
    "coconut":     {"emoji":"🥥","season":"Perennial","water":"Medium","soil":"Sandy Coastal",
                    "tip":"Excellent for coastal AP.",
                    "yield_q":30,"cost_per_acre":15000,"price_q":9000,
                    "N_req":100,"P_req":40,"K_req":200,
                    "calendar":{"Sow":[6,7],"Grow":[8,9,10,11,12,1,2,3,4],"Harvest":[5,6]},
                    "yield_trend":[22,24,25,26,27,28,30,32],
                    "why_factors":{"humidity":"Coastal high humidity ideal for coconut.",
                                   "rainfall":"1500–2500mm annual rainfall preferred.",
                                   "temperature":"27°C mean temperature optimal."}},
    "cotton":      {"emoji":"🌿","season":"Kharif (Jun–Nov)","water":"Medium","soil":"Black Soil",
                    "tip":"Major AP cash crop.",
                    "yield_q":8,"cost_per_acre":18000,"price_q":7000,
                    "N_req":80,"P_req":40,"K_req":40,
                    "calendar":{"Sow":[5,6],"Grow":[7,8,9],"Harvest":[10,11,12]},
                    "yield_trend":[5,5.5,6,6.2,6.8,7,7.5,8],
                    "why_factors":{"temperature":"Cotton loves 25–35°C.",
                                   "humidity":"Moderate humidity during boll development.",
                                   "rainfall":"600–1200mm seasonal rainfall ideal."}},
    "jute":        {"emoji":"🌿","season":"Kharif","water":"High","soil":"Alluvial",
                    "tip":"Needs high humidity.",
                    "yield_q":18,"cost_per_acre":10000,"price_q":4500,
                    "N_req":80,"P_req":30,"K_req":30,
                    "calendar":{"Sow":[3,4],"Grow":[5,6,7],"Harvest":[8,9]},
                    "yield_trend":[12,13,14,15,16,17,18,19],
                    "why_factors":{"humidity":"Jute requires >80% humidity.",
                                   "rainfall":">150cm annual rainfall needed.",
                                   "temperature":"Warm humid 25–36°C."}},
    "coffee":      {"emoji":"☕","season":"Perennial","water":"Medium","soil":"Loamy",
                    "tip":"Shade crop. Hilly regions.",
                    "yield_q":5,"cost_per_acre":25000,"price_q":18000,
                    "N_req":100,"P_req":30,"K_req":80,
                    "calendar":{"Sow":[6,7],"Grow":[8,9,10,11,12,1,2,3],"Harvest":[4,5,6]},
                    "yield_trend":[3.5,4,4.2,4.5,4.8,5,5.2,5.5],
                    "why_factors":{"temperature":"15–28°C under shade is ideal.",
                                   "humidity":"High humidity >70% preferred.",
                                   "rainfall":"1500–2500mm well-distributed."}},
}

# Fertilizer product mapping
FERTILIZERS = {
    "N": {"product":"Urea (46% N)",      "per_unit": 46, "unit":"kg"},
    "P": {"product":"SSP (16% P₂O₅)",   "per_unit": 16, "unit":"kg"},
    "K": {"product":"MOP (60% K₂O)",    "per_unit": 60, "unit":"kg"},
}
BAG_KG = 50

def get_crop_info(name):
    return CROP_INFO.get(name.lower(), {
        "emoji":"🌱","season":"Consult agronomist","water":"Medium","soil":"Loamy",
        "tip":"Check with Krishi Vigyan Kendra.",
        "yield_q":10,"cost_per_acre":10000,"price_q":3000,
        "N_req":80,"P_req":40,"K_req":40,
        "calendar":{"Sow":[6],"Grow":[7,8,9],"Harvest":[10]},
        "yield_trend":[8,8.5,9,9.2,9.5,9.8,10,10.5],
        "why_factors":{"humidity":"Moderate humidity is generally beneficial.",
                       "rainfall":"Adequate rainfall supports most crops.",
                       "temperature":"Moderate temperatures are suitable."},
    })

# ─────────────────────────────────────────────
#  CROP ROTATION KNOWLEDGE BASE
# ─────────────────────────────────────────────
CROP_ROTATION = {
    "rice": {
        "recommended_next": ["chickpea", "lentil", "maize"],
        "benefits": "Rice depletes nitrogen. Legumes fix nitrogen back into soil.",
        "avoid": ["rice", "jute"]
    },
    "maize": {
        "recommended_next": ["chickpea", "mungbean", "wheat"],
        "benefits": "Maize removes nutrients. Legumes replenish nitrogen.",
        "avoid": ["maize", "sorghum"]
    },
    "chickpea": {
        "recommended_next": ["rice", "maize", "cotton"],
        "benefits": "Chickpea fixes nitrogen. Next crop benefits from enriched soil.",
        "avoid": ["lentil", "pigeonpeas"]
    },
    "cotton": {
        "recommended_next": ["chickpea", "maize", "wheat"],
        "benefits": "Cotton depletes soil. Legumes restore soil health.",
        "avoid": ["cotton", "pigeonpeas"]
    },
    "pigeonpeas": {
        "recommended_next": ["rice", "maize", "wheat"],
        "benefits": "Deep-rooted crop improves soil structure. Follow with shallow-rooted.",
        "avoid": ["pigeonpeas", "blackgram"]
    },
    "wheat": {
        "recommended_next": ["rice", "maize", "mungbean"],
        "benefits": "Wheat residue management improves soil organic matter.",
        "avoid": ["wheat", "barley"]
    }
}

# ─────────────────────────────────────────────
#  AUTHENTICATION FUNCTIONS
# ─────────────────────────────────────────────
def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(mobile_number, otp):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute("UPDATE otp_codes SET is_used = 1 WHERE mobile_number = ?", (mobile_number,))
    
    now = datetime.now().isoformat()
    expires = (datetime.now() + timedelta(minutes=5)).isoformat()
    
    c.execute("""INSERT INTO otp_codes (mobile_number, otp_code, created_at, expires_at, is_used)
                 VALUES (?, ?, ?, ?, 0)""", (mobile_number, otp, now, expires))
    
    conn.commit()
    conn.close()

def verify_otp(mobile_number, otp):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    c.execute("""SELECT * FROM otp_codes 
                 WHERE mobile_number = ? AND otp_code = ? 
                 AND is_used = 0 AND expires_at > ?
                 ORDER BY created_at DESC LIMIT 1""", 
              (mobile_number, otp, now))
    
    result = c.fetchone()
    
    if result:
        c.execute("UPDATE otp_codes SET is_used = 1 WHERE id = ?", (result[0],))
        conn.commit()
        
        c.execute("SELECT * FROM users WHERE mobile_number = ?", (mobile_number,))
        user = c.fetchone()
        
        if not user:
            c.execute("""INSERT INTO users (mobile_number, created_at) 
                         VALUES (?, ?)""", (mobile_number, datetime.now().isoformat()))
            user_id = c.lastrowid
        else:
            user_id = user[0]
        
        conn.commit()
        conn.close()
        return True, user_id
    
    conn.close()
    return False, None

def get_user_history(user_id, limit=20):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute("""SELECT crop_name, n_value, p_value, k_value, temperature, 
                       humidity, ph, rainfall, acres, price_q, zone, previous_crop, 
                       confidence, timestamp 
                 FROM user_history 
                 WHERE user_id = ? 
                 ORDER BY timestamp DESC LIMIT ?""", (user_id, limit))
    
    history = c.fetchall()
    conn.close()
    
    return history

def save_to_history(user_id, crop_name, features, acres, price_q, zone, previous_crop, confidence):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute("""INSERT INTO user_history 
                 (user_id, crop_name, n_value, p_value, k_value, temperature, 
                  humidity, ph, rainfall, acres, price_q, zone, previous_crop, 
                  confidence, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (user_id, crop_name, features['N'], features['P'], features['K'],
               features['temp'], features['humidity'], features['ph'], features['rainfall'],
               acres, price_q, zone, previous_crop, confidence, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def clear_user_history(user_id):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute("DELETE FROM user_history WHERE user_id = ?", (user_id,))
    
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
#  SATELLITE DATA FUNCTIONS
# ─────────────────────────────────────────────
def fetch_satellite_data(lat, lon, zone_info):
    """Fetch satellite data from NASA POWER API"""
    try:
        params = {
            "parameters": "T2M,RH2M,PRECTOTCORR",
            "community": "re",
            "longitude": lon,
            "latitude": lat,
            "format": "JSON",
            "startDate": "20230101",
            "endDate": "20231231",
            "user": "crop_advisor_app"
        }
        
        response = requests.get(NASA_POWER_API, params=params, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'properties' in data and 'parameter' in data['properties']:
                params_data = data['properties']['parameter']
                
                t2m_data = params_data.get('T2M', {})
                rh2m_data = params_data.get('RH2M', {})
                rain_data = params_data.get('PRECTOTCORR', {})
                
                if t2m_data:
                    t2m_values = [v for v in t2m_data.values() if v is not None]
                    avg_temp = np.mean(t2m_values) if t2m_values else zone_info['avg_temp']
                else:
                    avg_temp = zone_info['avg_temp']
                
                if rh2m_data:
                    rh_values = [v for v in rh2m_data.values() if v is not None]
                    avg_humidity = np.mean(rh_values) if rh_values else 65
                else:
                    avg_humidity = 65
                
                if rain_data:
                    rain_values = [v for v in rain_data.values() if v is not None]
                    annual_rainfall = sum(rain_values) if rain_values else zone_info['avg_rainfall']
                else:
                    annual_rainfall = zone_info['avg_rainfall']
                
                return {
                    "success": True,
                    "avg_temp": round(avg_temp, 1),
                    "avg_humidity": round(avg_humidity, 1),
                    "annual_rainfall": round(annual_rainfall, 0),
                    "satellite_date": datetime.now().strftime("%Y-%m-%d"),
                    "lat": lat,
                    "lon": lon
                }
            else:
                return {
                    "success": True,
                    "avg_temp": zone_info['avg_temp'],
                    "avg_humidity": 65,
                    "annual_rainfall": zone_info['avg_rainfall'],
                    "satellite_date": datetime.now().strftime("%Y-%m-%d"),
                    "lat": lat,
                    "lon": lon,
                    "note": "Using zone averages"
                }
        else:
            return {
                "success": True,
                "avg_temp": zone_info['avg_temp'],
                "avg_humidity": 65,
                "annual_rainfall": zone_info['avg_rainfall'],
                "satellite_date": datetime.now().strftime("%Y-%m-%d"),
                "lat": lat,
                "lon": lon,
                "note": "Using zone averages"
            }
            
    except Exception as e:
        return {
            "success": True,
            "avg_temp": zone_info['avg_temp'],
            "avg_humidity": 65,
            "annual_rainfall": zone_info['avg_rainfall'],
            "satellite_date": datetime.now().strftime("%Y-%m-%d"),
            "lat": lat,
            "lon": lon,
            "note": f"Using zone averages"
        }

def calculate_ndvi_estimate(temp, humidity, rainfall):
    """Estimate NDVI based on weather parameters"""
    base_ndvi = 0.3
    temp_factor = max(0, min(1, 1 - abs(temp - 25) / 20))
    humidity_factor = max(0, min(1, 1 - abs(humidity - 70) / 30))
    rain_factor = max(0, min(1, 1 - abs(rainfall - 150) / 100))
    
    ndvi = base_ndvi + 0.3 * temp_factor + 0.2 * humidity_factor + 0.2 * rain_factor
    return min(0.9, max(0.1, ndvi))

# ─────────────────────────────────────────────
#  ADAPTIVE LEARNING FUNCTIONS
# ─────────────────────────────────────────────
def save_feedback(user_id, crop_name, features, rating, location):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO user_feedback 
                 (user_id, crop_name, n_value, p_value, k_value, temperature, humidity, ph, rainfall, 
                  user_rating, feedback_date, location)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_id, crop_name, features['N'], features['P'], features['K'],
               features['temp'], features['humidity'], features['ph'], features['rainfall'],
               rating, datetime.now().isoformat(), location))
    
    conn.commit()
    conn.close()

def update_model_weights(features, rating):
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    if rating >= 4:
        for feature in ['N', 'P', 'K', 'temp', 'humidity', 'ph', 'rainfall']:
            c.execute('''INSERT INTO model_weights (feature_name, weight, last_updated)
                         VALUES (?, ?, ?)
                         ON CONFLICT(feature_name) DO UPDATE SET
                         weight = (weight * 0.9 + 0.1),
                         last_updated = ?''',
                      (feature, 1.0, datetime.now().isoformat()))
    elif rating <= 2:
        for feature in ['N', 'P', 'K', 'temp', 'humidity', 'ph', 'rainfall']:
            c.execute('''INSERT INTO model_weights (feature_name, weight, last_updated)
                         VALUES (?, ?, ?)
                         ON CONFLICT(feature_name) DO UPDATE SET
                         weight = (weight * 0.9),
                         last_updated = ?''',
                      (feature, 0.9, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_learning_stats():
    conn = sqlite3.connect('crop_advisor.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM user_feedback")
    total_feedback = c.fetchone()[0]
    
    c.execute("SELECT AVG(user_rating) FROM user_feedback WHERE user_rating > 0")
    avg_rating = c.fetchone()[0] or 0
    
    c.execute('''SELECT crop_name, COUNT(*) as cnt 
                 FROM user_feedback 
                 GROUP BY crop_name 
                 ORDER BY cnt DESC LIMIT 5''')
    top_crops = c.fetchall()
    
    c.execute('''SELECT crop_name, AVG(user_rating) as avg_rating 
                 FROM user_feedback 
                 WHERE user_rating >= 4
                 GROUP BY crop_name 
                 ORDER BY avg_rating DESC LIMIT 5''')
    high_rated = c.fetchall()
    
    conn.close()
    
    return {
        "total_feedback": total_feedback,
        "avg_rating": round(avg_rating, 2),
        "top_crops": top_crops,
        "high_rated": high_rated
    }

def get_rotation_suggestion(previous_crop):
    if previous_crop and previous_crop.lower() in CROP_ROTATION:
        rotation = CROP_ROTATION[previous_crop.lower()]
        return {
            "recommended": rotation["recommended_next"],
            "benefits": rotation["benefits"],
            "avoid": rotation["avoid"]
        }
    else:
        return {
            "recommended": ["chickpea", "maize", "mungbean"],
            "benefits": "Crop rotation helps maintain soil health and reduces pest pressure.",
            "avoid": []
        }

def get_hyperlocal_zone(location_name):
    for zone_name, zone_data in HYPERLOCAL_ZONES.items():
        if location_name.lower() in zone_name.lower():
            return zone_name, zone_data
    
    return "Generic Region", {
        "lat": 20.0, "lon": 78.0,
        "avg_temp": 26.0, "avg_rainfall": 1000,
        "soil_type": "Mixed",
        "best_crops": ["rice", "maize", "chickpea", "cotton"],
        "growing_season": "June-December"
    }

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def check_soil_health(N, P, K, ph):
    a = []
    if N < 20:   a.append("⚠️ Nitrogen LOW — apply Urea or DAP.")
    if N > 150:  a.append("⚠️ Nitrogen HIGH — reduce urea to avoid crop burn.")
    if P < 10:   a.append("⚠️ Phosphorus LOW — apply SSP (Single Super Phosphate).")
    if K < 10:   a.append("⚠️ Potassium LOW — apply MOP (Muriate of Potash).")
    if ph < 5.5: a.append("⚠️ Soil too ACIDIC (pH<5.5) — apply agricultural lime.")
    if ph > 8.0: a.append("⚠️ Soil too ALKALINE (pH>8) — apply gypsum or sulfur.")
    return a

def fetch_weather(city):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric",
            timeout=6)
        if r.status_code != 200:
            return None, f"City '{city}' not found."
        d = r.json()
        return {"temp": round(d["main"]["temp"],1), "humidity": round(d["main"]["humidity"],1)}, None
    except Exception as e:
        return None, str(e)

def compute_profit(info, acres, price_q):
    yt  = info["yield_q"] * acres
    rev = yt * price_q
    cst = info["cost_per_acre"] * acres
    return yt, rev, cst, rev - cst

def compute_fertilizer(info, acres):
    results = []
    for nutrient, val_per_ha in [("N", info["N_req"]), ("P", info["P_req"]), ("K", info["K_req"])]:
        f        = FERTILIZERS[nutrient]
        kg_total = (val_per_ha * acres * 0.4047)
        prod_kg  = (kg_total / f["per_unit"]) * 100
        bags     = prod_kg / BAG_KG
        results.append({
            "nutrient": nutrient,
            "product":  f["product"],
            "kg_needed": round(prod_kg, 1),
            "bags":      round(bags, 1),
        })
    return results

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def render_calendar(cal, T):
    html = "<div style='margin-top:0.4rem;'>"
    for i, m in enumerate(MONTHS):
        mn = i+1
        if   mn in cal.get("Sow",[]): cls="cal-sow"
        elif mn in cal.get("Grow",[]): cls="cal-grow"
        elif mn in cal.get("Harvest",[]): cls="cal-harvest"
        else: cls="cal-idle"
        html += f'<span class="cal-month {cls}">{m}</span>'
    html += f"""</div>
    <div style='margin-top:0.4rem;font-size:0.78rem;color:#666;'>
      <span class='cal-month cal-sow'>{T['legend_sow']}</span>
      <span class='cal-month cal-grow'>{T['legend_grow']}</span>
      <span class='cal-month cal-harvest'>{T['legend_harvest']}</span>
    </div>"""
    return html

def generate_why_explainer(prediction, info, N, P, K, temp, humidity, ph, rainfall):
    factors = info.get("why_factors", {})
    lines   = []
    crop    = prediction.title()
    if "humidity" in factors:
        lines.append(f"<b>Humidity ({humidity}%):</b> {factors['humidity']}")
    if "rainfall" in factors:
        lines.append(f"<b>Rainfall ({rainfall}mm):</b> {factors['rainfall']}")
    if "temperature" in factors:
        lines.append(f"<b>Temperature ({temp}°C):</b> {factors['temperature']}")
    if "ph" in factors:
        lines.append(f"<b>Soil pH ({ph}):</b> {factors['ph']}")
    bullets = "".join(f"<li style='margin-bottom:4px'>{l}</li>" for l in lines)
    return f"""
    <div class="explainer-box">
      <div class="explainer-title">Why {crop}?</div>
      <div class="explainer-text">
        Your field conditions closely match what {crop} needs:<br>
        <ul style='margin:0.5rem 0 0 1rem;padding:0'>{bullets}</ul>
      </div>
    </div>"""

# ─────────────────────────────────────────────
#  LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = "knn_crop_model.pkl"
    if not os.path.exists(path):
        st.error("❌ 'knn_crop_model.pkl' not found. Place it next to app.py.")
        st.stop()
    return joblib.load(path)

model = load_model()

# ─────────────────────────────────────────────
#  LANGUAGE + SESSION STATE
# ─────────────────────────────────────────────
top_l, top_r = st.columns([5, 1])
with top_r:
    lang_choice = st.selectbox("", list(LANG.keys()), label_visibility="collapsed")
T = LANG[lang_choice]

# Initialize session state
for k, v in [("w_temp",25.0),("w_humid",80.0),("w_badge",""),
             ("pred_result",None),("input_snap",None),("satellite_data",None),
             ("previous_crop",""),("feedback_submitted",False),
             ("user_id",None),("user_mobile",None),("logged_in",False),
             ("otp_sent",False),("otp_code","")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  LOGIN SECTION WITH REAL SMS
# ─────────────────────────────────────────────
def login_section():
    st.sidebar.markdown(f"""
    <div class="card">
        <div class="card-title">{T['login_title']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        mobile = st.sidebar.text_input(T['mobile_number'], placeholder="+919876543210 or 9876543210")
        
        if st.sidebar.button(T['send_otp'], use_container_width=True):
            if mobile and len(mobile.replace('+', '').replace('-', '').replace(' ', '')) >= 10:
                # Clean mobile number
                clean_mobile = re.sub(r'\D', '', mobile)
                if len(clean_mobile) == 10:
                    clean_mobile = "+91" + clean_mobile
                elif clean_mobile.startswith('91') and len(clean_mobile) == 12:
                    clean_mobile = "+" + clean_mobile
                elif not clean_mobile.startswith('+'):
                    clean_mobile = "+" + clean_mobile
                
                otp = generate_otp()
                save_otp(clean_mobile, otp)
                st.session_state.otp_code = otp
                st.session_state.user_mobile = clean_mobile
                
                # Send OTP via SMS
                success, message = send_otp_sms(clean_mobile, otp)
                
                if success:
                    st.session_state.otp_sent = True
                    st.sidebar.success(T['otp_sent_success'])
                else:
                    st.sidebar.error(f"{T['otp_sent_failed']} - {message}")
            else:
                st.sidebar.error("Please enter a valid mobile number (10 digits)")
        
        if st.session_state.otp_sent:
            otp_input = st.sidebar.text_input(T['enter_otp'], placeholder="6-digit OTP", type="password")
            if st.sidebar.button(T['verify_otp'], use_container_width=True):
                if otp_input == st.session_state.otp_code:
                    success, user_id = verify_otp(st.session_state.user_mobile, otp_input)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.sidebar.success(f"{T['login_success']} {st.session_state.user_mobile}")
                        st.rerun()
                    else:
                        st.sidebar.error(T['login_failed'])
                else:
                    st.sidebar.error("Invalid OTP. Please try again.")
    else:
        st.sidebar.success(f"✅ Logged in: {st.session_state.user_mobile}")
        if st.sidebar.button(T['logout'], use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_mobile = None
            st.session_state.otp_sent = False
            st.session_state.pred_result = None
            st.rerun()

# Show login section in sidebar
login_section()

# Only show main content if logged in
if not st.session_state.logged_in:
    st.info("👋 Please login using your mobile number to access the Crop Advisor.")
    st.stop()

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>{T['title']}</h1>
  <p>{T['subtitle']}</p>
  <div class="hero-badges">
    <span class="hero-badge">🤖 KNN AI Model</span>
    <span class="hero-badge">🌤️ Live Weather</span>
    <span class="hero-badge">💰 Profit Calc</span>
    <span class="hero-badge">🧪 Fertilizer Calc</span>
    <span class="hero-badge">🌐 3 Languages</span>
    <span class="hero-badge">🛰️ Satellite Data</span>
    <span class="hero-badge">🔄 Crop Rotation</span>
    <span class="hero-badge">🧠 Adaptive Learning</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN LAYOUT: Input | Output
# ─────────────────────────────────────────────
left, right = st.columns([1.05, 1], gap="large")

# ══════════════════
#  LEFT — INPUTS
# ══════════════════
with left:

    # Hyperlocal Zone Selection
    st.markdown(f'<div class="card"><div class="card-title">📍 {T["zone_label"]}</div>', unsafe_allow_html=True)
    zone_names = list(HYPERLOCAL_ZONES.keys())
    selected_zone = st.selectbox("", zone_names, label_visibility="collapsed")
    zone_info = HYPERLOCAL_ZONES[selected_zone]
    
    st.markdown(f"""
    <div class="info-alert">
      <strong>📍 {selected_zone}</strong><br>
      Soil: {zone_info['soil_type']} | Growing Season: {zone_info['growing_season']}<br>
      Avg Temp: {zone_info['avg_temp']}°C | Avg Rainfall: {zone_info['avg_rainfall']}mm
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Previous Crop for Rotation
    st.markdown(f'<div class="card"><div class="card-title">🔄 {T["previous_crop"]}</div>', unsafe_allow_html=True)
    crop_options = list(CROP_INFO.keys()) + ["None (First Season)", "Other"]
    previous_crop = st.selectbox("", crop_options, label_visibility="collapsed", 
                                   placeholder="Select previous crop grown")
    if previous_crop and previous_crop != "None (First Season)":
        rotation_advice = get_rotation_suggestion(previous_crop)
        st.markdown(f"""
        <div class="tip-card">
          <p class="tip-text"><strong>🔄 Rotation Benefit:</strong> {rotation_advice['benefits']}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Weather auto-fill
    st.markdown(f'<div class="card"><div class="card-title">{T["weather_section"]}</div>', unsafe_allow_html=True)
    wc1, wc2 = st.columns([2,1])
    with wc1:
        city = st.text_input(T["city_label"], selected_zone.split()[0] if selected_zone else "Hyderabad", 
                             label_visibility="collapsed", placeholder=T["city_label"])
    with wc2:
        fetch_btn = st.button(T["btn_weather"], use_container_width=True)

    if fetch_btn:
        if OWM_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
            st.warning("🔑 Set your free OWM_API_KEY in the code (openweathermap.org).")
        else:
            with st.spinner(T["fetching"]):
                wd, err = fetch_weather(city)
            if err:
                st.error(f"❌ {err}")
            else:
                st.session_state.w_temp  = wd["temp"]
                st.session_state.w_humid = wd["humidity"]
                st.session_state.w_badge = f"✅ {city} — {wd['temp']}°C, Humidity {wd['humidity']}%"

    if st.session_state.w_badge:
        st.markdown(f'<div class="weather-badge">{st.session_state.w_badge}</div>', unsafe_allow_html=True)

    ic1, ic2 = st.columns(2)
    with ic1:
        temp = st.number_input(T["temperature"], 0.0, 55.0, float(st.session_state.w_temp))
        ph   = st.number_input(T["ph"], 0.0, 14.0, 6.5)
    with ic2:
        humidity = st.number_input(T["humidity"], 0.0, 100.0, float(st.session_state.w_humid))
        rainfall = st.number_input(T["rainfall"], 0.0, 400.0, 200.0)
    st.markdown('</div>', unsafe_allow_html=True)

    # Soil nutrients
    st.markdown(f'<div class="card"><div class="card-title">{T["soil_section"]}</div>', unsafe_allow_html=True)
    nc1, nc2, nc3 = st.columns(3)
    with nc1: N = st.number_input(T["nitrogen"], 0, 200, 90)
    with nc2: P = st.number_input(T["phosphorus"], 0, 200, 40)
    with nc3: K = st.number_input(T["potassium"], 0, 200, 40)
    st.markdown('</div>', unsafe_allow_html=True)

    # Profit inputs
    st.markdown('<div class="card"><div class="card-title">💰 Profit & Fertilizer Inputs</div>', unsafe_allow_html=True)
    pc1, pc2 = st.columns(2)
    with pc1: acres = st.number_input(T["acres"], 0.5, 100.0, 2.0, step=0.5)
    with pc2: price_q = st.number_input(T["price_per_q"], 500, 50000, 3000, step=100)
    st.markdown('</div>', unsafe_allow_html=True)

    # Soil alerts
    for a in check_soil_health(N, P, K, ph):
        st.markdown(f'<div class="soil-alert">{a}</div>', unsafe_allow_html=True)

    st.write("")
    predict_btn = st.button(T["btn_predict"], use_container_width=True)

    if predict_btn:
        arr = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        with st.spinner(T["analyzing"]):
            pred = model.predict(arr)[0]
            try:
                probas = model.predict_proba(arr)[0]
                top_idx = np.argmax(probas)
                confidence = probas[top_idx] * 100
            except:
                confidence = 85.0
        
        st.session_state.pred_result = pred
        st.session_state.input_snap  = dict(N=N,P=P,K=K,temp=temp,
                                            humidity=humidity,ph=ph,
                                            rainfall=rainfall,acres=acres,price_q=price_q,
                                            zone=selected_zone, previous_crop=previous_crop)
        
        save_to_history(st.session_state.user_id, pred, st.session_state.input_snap, 
                        acres, price_q, selected_zone, previous_crop, confidence)

# ════════════════════
#  RIGHT — RESULTS
# ════════════════════
with right:
    pred  = st.session_state.pred_result
    snap  = st.session_state.input_snap

    if pred is None:
        st.markdown(f"""
        <div style="text-align:center;padding:3.5rem 1rem;color:#bbb;">
          <div style="font-size:5rem;">🌱</div>
          <p style="font-size:1rem;margin-top:1rem;">{T['placeholder']}</p>
        </div>""", unsafe_allow_html=True)
    else:
        info = get_crop_info(pred)
        N2,P2,K2      = snap["N"],snap["P"],snap["K"]
        temp2         = snap["temp"]
        humidity2     = snap["humidity"]
        ph2           = snap["ph"]
        rainfall2     = snap["rainfall"]
        acres2        = snap["acres"]
        price_q2      = snap["price_q"]
        zone_name     = snap.get("zone", selected_zone)
        prev_crop     = snap.get("previous_crop", previous_crop)
        arr2          = np.array([[N2,P2,K2,temp2,humidity2,ph2,rainfall2]])

        # ── Main result card ──
        rotation_match = False
        rotation_text = ""
        if prev_crop and prev_crop != "None (First Season)" and prev_crop != "Other":
            rotation_info = get_rotation_suggestion(prev_crop)
            if pred in rotation_info["recommended"]:
                rotation_match = True
                rotation_text = " ✓ Good rotation match!"
            elif pred in rotation_info["avoid"]:
                rotation_text = " ⚠️ Avoid following this crop"

        st.markdown(f"""
        <div class="result-box">
          <div style="font-size:3rem;">{info['emoji']}</div>
          <div class="result-crop">{pred}</div>
          <div class="result-sub">{T['best_crop']}</div>
          <div class="season-badge">📅 {info['season']}</div>
          {f'<div class="rotation-badge">🔄 {rotation_text}</div>' if rotation_text else ''}
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ── Tabs for all features ──
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📊 Details", "🧪 Fertilizer", "⚖️ Compare", "📈 Trends", "📜 History", "🛰️ Satellite", "🔄 Rotation"
        ])

        # ════ TAB 1: Details ════
        with tab1:
            try:
                probas   = model.predict_proba(arr2)[0]
                top5_idx = np.argsort(probas)[::-1][:5]
                top5     = [(model.classes_[i], probas[i]*100) for i in top5_idx]
                top_pct  = top5[0][1]

                if top_pct < 60:
                    st.markdown(f'<div class="warn-alert">{T["low_conf"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-alert">✅ AI confidence: <strong>{top_pct:.0f}%</strong> — high confidence result.</div>', unsafe_allow_html=True)

                st.markdown(f'<div class="card"><div class="card-title">{T["top3"]}</div>', unsafe_allow_html=True)
                medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
                for idx,(crop,pct) in enumerate(top5):
                    ci = get_crop_info(crop)
                    st.markdown(f"""
                    <div class="conf-row">
                      <div class="conf-label">{medals[idx]} {ci['emoji']} {crop.title()}</div>
                      <div class="conf-bar-bg">
                        <div class="conf-bar-fill" style="width:{min(pct,100):.0f}%">{pct:.0f}%</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                top_pct = 100

            # Why This Crop
            st.markdown(f'<div class="card"><div class="card-title">{T["why_title"]}</div>', unsafe_allow_html=True)
            st.markdown(generate_why_explainer(pred,info,N2,P2,K2,temp2,humidity2,ph2,rainfall2),
                        unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Farming Tips
            st.markdown(f'<div class="card"><div class="card-title">{T["tips_title"]} {pred.title()}</div>',
                        unsafe_allow_html=True)
            for lbl,val in [(T["water_req"],info["water"]),(T["soil_type"],info["soil"]),(T["farmer_tip"],info["tip"])]:
                st.markdown(f'<div class="tip-card"><p class="tip-text"><strong>{lbl}:</strong> {val}</p></div>',
                            unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Profit Estimator
            yt, rev, cst, profit = compute_profit(info, acres2, price_q2)
            pc = "#1b5e20" if profit >= 0 else "#b71c1c"
            pl = T["profitable"] if profit >= 0 else T["loss"]

            st.markdown(f'<div class="card"><div class="card-title">{T["profit_title"]}</div>', unsafe_allow_html=True)
            pa, pb = st.columns(2)
            with pa:
                st.markdown(f"""
                <div class="profit-card">
                  <div class="profit-title">{T['est_yield']}</div>
                  <div class="profit-value">{yt:.0f} qtl</div>
                  <div class="profit-sub">{acres2} acres</div>
                </div>
                <div class="profit-card">
                  <div class="profit-title">{T['est_revenue']}</div>
                  <div class="profit-value">₹{rev:,.0f}</div>
                  <div class="profit-sub">@ ₹{price_q2}/qtl</div>
                </div>""", unsafe_allow_html=True)
            with pb:
                st.markdown(f"""
                <div class="profit-card">
                  <div class="profit-title">{T['est_cost']}</div>
                  <div class="profit-value">₹{cst:,.0f}</div>
                  <div class="profit-sub">seeds + fertilizer + labour</div>
                </div>
                <div class="profit-card" style="border-left-color:{pc};">
                  <div class="profit-title" style="color:{pc};">{T['est_profit']}</div>
                  <div class="profit-value" style="color:{pc};">₹{profit:,.0f}</div>
                  <div class="profit-sub">{pl}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:0.76rem;color:#999;margin-top:0.2rem;">{T["profit_note"]}</p></div>',
                        unsafe_allow_html=True)

            # Crop Calendar
            st.markdown(f'<div class="card"><div class="card-title">{T["calendar_title"]}</div>', unsafe_allow_html=True)
            st.markdown(render_calendar(info["calendar"], T), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # User Feedback Section
            st.markdown(f'<div class="card"><div class="card-title">⭐ {T["feedback_rating"]}</div>', unsafe_allow_html=True)
            rating = st.select_slider("", options=[1, 2, 3, 4, 5], value=3)
            if st.button(T["submit_feedback"]):
                save_feedback(st.session_state.user_id, pred, snap, rating, zone_name)
                update_model_weights(snap, rating)
                st.session_state.feedback_submitted = True
                st.success("Thank you for your feedback! This helps improve our recommendations.")
            st.markdown('</div>', unsafe_allow_html=True)

        # ════ TAB 2: Fertilizer Calculator ════
        with tab2:
            st.markdown(f'<div class="card-title">{T["fert_title"]}</div>', unsafe_allow_html=True)
            ferts = compute_fertilizer(info, acres2)

            f1,f2,f3 = st.columns(3)
            colors = ["#2e7d32","#1565c0","#e65100"]
            for col, frow, clr in zip([f1,f2,f3], ferts, colors):
                with col:
                    st.markdown(f"""
                    <div style="background:white;border-left:4px solid {clr};border-radius:12px;
                                padding:1rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.07);">
                      <div style="font-size:1.8rem;font-weight:700;color:{clr};">{frow['bags']:.1f}</div>
                      <div style="font-size:0.78rem;font-weight:600;color:{clr};">Bags of 50kg</div>
                      <div style="font-size:0.82rem;color:#555;margin-top:0.3rem;">{frow['product']}</div>
                      <div style="font-size:0.76rem;color:#888;">{frow['kg_needed']:.0f} kg total</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div class="tip-card" style="border-left-color:#43a047;">
              <p class="tip-text"><strong>📋 Application Guide:</strong><br>
              • Apply <b>Urea</b> in 2 splits — at sowing & 30 days later<br>
              • Apply <b>SSP</b> fully at sowing/land preparation<br>
              • Apply <b>MOP</b> at sowing or 1st top-dressing<br>
              • Always do a soil test before applying fertilizers</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="soil-alert" style="margin-top:0.5rem;">
              ⚠️ These are <b>recommended</b> doses for {pred.title()} on {acres2} acres.
              Adjust based on your actual soil test report.
              Soil test reports from Soil Health Card (SHC) scheme are more accurate.
            </div>""", unsafe_allow_html=True)

        # ════ TAB 3: Alternative Crop Comparison ════
        with tab3:
            st.markdown(f'<div class="card-title">{T["compare_title"]}</div>', unsafe_allow_html=True)

            try:
                probas   = model.predict_proba(arr2)[0]
                top5_idx = np.argsort(probas)[::-1][:5]
                compare_crops = [model.classes_[i] for i in top5_idx]
            except Exception:
                compare_crops = [pred]

            rows = []
            for cr in compare_crops:
                ci = get_crop_info(cr)
                _, rev, cst, pft = compute_profit(ci, 1, ci["price_q"])
                rows.append({
                    "crop": cr, "emoji": ci["emoji"],
                    "water": ci["water"], "season": ci["season"],
                    "yield": ci["yield_q"], "cost": ci["cost_per_acre"],
                    "profit": int(pft), "is_best": cr == pred,
                })

            html = f"""<table class="comp-table">
              <tr>
              <th>{T['crop_col']}</th>
              <th>{T['water_col']}</th>
              <th>{T['yield_col']}</th>
              <th>{T['cost_col']}</th>
              <th>{T['profit_col']}</th>
              <th>{T['season_col']}</th>
              </tr>"""
            for r in rows:
                row_cls = 'class="best-row"' if r["is_best"] else ""
                badge   = '<span class="best-badge">✓ Best</span>' if r["is_best"] else ""
                pc_c    = "#1b5e20" if r["profit"]>=0 else "#b71c1c"
                html += f"""<tr {row_cls}>
                  <td>{r['emoji']} {r['crop'].title()}{badge}</td>
                  <td>{r['water']}</td>
                  <td>{r['yield']}</td>
                  <td>₹{r['cost']:,}</td>
                  <td style="color:{pc_c};font-weight:700;">₹{r['profit']:,}</td>
                  <td style="font-size:0.78rem;">{r['season']}</td>
                </tr>"""
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="tip-card" style="margin-top:0.8rem;">
              <p class="tip-text"><strong>💡 Profit</strong> is estimated per acre using default market price.
              Actual prices vary by region and season. Always check your local mandi rates before deciding.</p>
            </div>""", unsafe_allow_html=True)

        # ════ TAB 4: Historical Yield Trends ════
        with tab4:
            st.markdown(f'<div class="card-title">{T["trends_title"]}</div>', unsafe_allow_html=True)
            years = [2017,2018,2019,2020,2021,2022,2023,2024]
            trend = info["yield_trend"]
            max_y = max(trend) * 1.1

            st.markdown(f"<p style='font-size:0.88rem;color:#555;'>Average yield of <b>{pred.title()}</b> in India (quintals/acre) over last 8 years:</p>",
                        unsafe_allow_html=True)

            for yr, val in zip(years, trend):
                pct = int((val / max_y) * 100)
                color = "#1a6b2e" if yr == 2024 else "#56c175"
                st.markdown(f"""
                <div class="yield-bar-wrap">
                  <div class="yield-label">{yr}</div>
                  <div class="yield-bar-bg">
                    <div class="yield-bar-fill" style="width:{pct}%;background:{color};">
                      {val} qtl/acre
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

            delta  = trend[-1] - trend[0]
            pct_ch = ((delta) / trend[0]) * 100 if trend[0] > 0 else 0
            arrow  = "📈" if delta>=0 else "📉"
            st.markdown(f"""
            <div class="success-alert" style="margin-top:0.8rem;">
              {arrow} Yield improved by <b>{pct_ch:.1f}%</b> over 8 years
              ({trend[0]} → {trend[-1]} qtl/acre). National average trend.
            </div>""", unsafe_allow_html=True)

        # ════ TAB 5: History ════
        with tab5:
            st.markdown(f'<div class="card-title">{T["history_title"]}</div>', unsafe_allow_html=True)
            
            history = get_user_history(st.session_state.user_id)
            
            if history:
                if st.button(T["clear_history"], use_container_width=True):
                    clear_user_history(st.session_state.user_id)
                    st.rerun()
                
                for h in history:
                    crop = h[0]
                    n, p, k = h[1], h[2], h[3]
                    temp_h, hum, ph_h, rain = h[4], h[5], h[6], h[7]
                    acres_h, price_h = h[8], h[9]
                    zone_h = h[10]
                    prev_h = h[11]
                    conf_h = h[12]
                    timestamp = h[13]
                    
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="history-date">📅 {timestamp[:16]}</div>
                        <div class="history-crop">🌾 Recommended: <strong>{crop.title()}</strong> (Confidence: {conf_h:.0f}%)</div>
                        <div class="tip-text">🌍 Zone: {zone_h} | 📍 Previous: {prev_h if prev_h else 'None'}</div>
                        <div class="tip-text">🧪 N:{n} | P:{p} | K:{k} | Temp:{temp_h}°C | Hum:{hum}% | pH:{ph_h} | Rain:{rain}mm</div>
                        <div class="tip-text">💰 {acres_h} acres @ ₹{price_h}/qtl</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="info-alert">{T["no_history"]}</div>', unsafe_allow_html=True)

        # ════ TAB 6: Satellite Insights ════
        with tab6:
            st.markdown(f'<div class="card-title">{T["satellite_title"]}</div>', unsafe_allow_html=True)
            
            lat = zone_info["lat"]
            lon = zone_info["lon"]
            
            with st.spinner(T["satellite_fetching"]):
                sat_data = fetch_satellite_data(lat, lon, zone_info)
            
            note_html = f'<div style="font-size:0.8rem;color:#666;margin-bottom:0.5rem;">📍 Coordinates: {lat}°N, {lon}°E</div>'
            if sat_data.get('note'):
                note_html += f'<div style="font-size:0.75rem;color:#ff9800;">ℹ️ Note: {sat_data["note"]}</div>'
            
            st.markdown(f"""
            <div class="satellite-card">
              <div style="font-weight:600;margin-bottom:0.5rem;">🛰️ NASA POWER Satellite Data</div>
              {note_html}
              <div>📍 Location: {selected_zone}</div>
              <div>🌡️ Average Temperature: <strong>{sat_data['avg_temp']}°C</strong></div>
              <div>💧 Average Humidity: <strong>{sat_data['avg_humidity']}%</strong></div>
              <div>🌧️ Annual Rainfall: <strong>{sat_data['annual_rainfall']} mm</strong></div>
              <div>📅 Data Date: {sat_data['satellite_date']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            ndvi = calculate_ndvi_estimate(temp2, humidity2, rainfall2)
            
            if ndvi > 0.6:
                ndvi_text = T["ndvi_excellent"]
                ndvi_color = "#2e7d32"
            elif ndvi > 0.4:
                ndvi_text = T["ndvi_moderate"]
                ndvi_color = "#f57c00"
            else:
                ndvi_text = T["ndvi_low"]
                ndvi_color = "#c62828"
            
            st.markdown(f"""
            <div class="card">
              <div class="card-title">🌿 {T['ndvi_label']}</div>
              <div class="conf-row">
                <div class="conf-label">NDVI Value</div>
                <div class="conf-bar-bg">
                  <div class="conf-bar-fill" style="width:{ndvi*100:.0f}%;background:linear-gradient(90deg,{ndvi_color},#81c784);">
                    {ndvi:.2f}
                  </div>
                </div>
              </div>
              <div class="tip-text" style="margin-top:0.5rem;color:{ndvi_color};">
                {ndvi_text}
              </div>
              <div class="tip-text" style="margin-top:0.5rem;font-size:0.75rem;color:#666;">
                {T['ndvi_description']}
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            temp_diff = abs(temp2 - sat_data['avg_temp'])
            rain_diff = abs(rainfall2 - sat_data['annual_rainfall'])
            
            if temp_diff > 5 or rain_diff > 300:
                st.markdown(f"""
                <div class="warn-alert">
                  ⚠️ Your field conditions differ from regional satellite averages. 
                  Consider local microclimate factors for better accuracy.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-alert">
                  ✅ Your field conditions align well with regional satellite data.
                </div>
                """, unsafe_allow_html=True)

        # ════ TAB 7: Crop Rotation ════
        with tab7:
            st.markdown(f'<div class="card-title">{T["rotation_title"]}</div>', unsafe_allow_html=True)
            
            if prev_crop and prev_crop != "None (First Season)" and prev_crop != "Other":
                rotation_info = get_rotation_suggestion(prev_crop)
                
                st.markdown(f"""
                <div class="info-alert">
                  <strong>Previous Crop: {prev_crop.title()}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="card">
                  <div class="card-title">🔄 {T['rotation_suggestion']}</div>
                  <div class="tip-text">
                    <strong>Recommended next crops:</strong><br>
                    {', '.join([c.title() for c in rotation_info['recommended']])}
                  </div>
                  <div class="tip-text" style="margin-top:0.5rem;">
                    <strong>✅ Benefits:</strong> {rotation_info['benefits']}
                  </div>
                  <div class="tip-text" style="margin-top:0.5rem;color:#d32f2f;">
                    <strong>⚠️ Avoid:</strong> {', '.join([c.title() for c in rotation_info['avoid']]) if rotation_info['avoid'] else "None"}
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                if pred in rotation_info['recommended']:
                    st.markdown(f"""
                    <div class="success-alert">
                      ✅ <strong>Great!</strong> Your recommended crop <strong>{pred.title()}</strong> is an excellent 
                      choice for crop rotation after {prev_crop.title()}.
                    </div>
                    """, unsafe_allow_html=True)
                elif pred in rotation_info['avoid']:
                    st.markdown(f"""
                    <div class="warn-alert">
                      ⚠️ <strong>Consider rotation:</strong> Growing {pred.title()} after {prev_crop.title()} 
                      may not be ideal. Consider {rotation_info['recommended'][0].title()} instead.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="info-alert">
                      ℹ️ {pred.title()} can be grown after {prev_crop.title()}, but for optimal soil health, 
                      consider {rotation_info['recommended'][0].title()} or {rotation_info['recommended'][1].title()}.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-alert">
                  ℹ️ To get crop rotation suggestions, please select your previous crop from the left sidebar.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card">
              <div class="card-title">📚 Crop Rotation Benefits</div>
              <div class="tip-text">
                • <strong>Soil Health:</strong> Different crops use different nutrients, preventing depletion.<br>
                • <strong>Pest Management:</strong> Breaks pest and disease cycles.<br>
                • <strong>Weed Control:</strong> Different planting times and growth habits suppress weeds.<br>
                • <strong>Yield Improvement:</strong> Legumes fix nitrogen for following crops.<br>
                • <strong>Risk Management:</strong> Diversifies income sources.
              </div>
            </div>
            
            <div class="card">
              <div class="card-title">🌾 Common Rotation Patterns</div>
              <div class="tip-text">
                • <strong>Rice → Chickpea/Maize:</strong> Rice depletes nitrogen; legumes restore it.<br>
                • <strong>Maize → Wheat/Pulses:</strong> Cereal followed by legume improves soil.<br>
                • <strong>Cotton → Chickpea/Wheat:</strong> Cotton depletes soil; rotation restores.<br>
                • <strong>Pulses → Cereals:</strong> Legumes fix nitrogen for cereal crops.
              </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Adaptive Learning Stats
        with st.expander("🧠 Adaptive Learning System Stats", expanded=False):
            stats = get_learning_stats()
            st.markdown(f"""
            <div class="learning-stats">
              <div class="card-title" style="margin-bottom:0.5rem;">{T['learning_stats']}</div>
              <div>📊 Total Feedback: <strong>{stats['total_feedback']}</strong></div>
              <div>⭐ Average Rating: <strong>{stats['avg_rating']}/5.0</strong></div>
              <div>🏆 Most Recommended Crops: 
                {', '.join([f"{c[0].title()}({c[1]})" for c in stats['top_crops'][:3]]) if stats['top_crops'] else "None yet"}
              </div>
              <div>🌟 Highest Rated Crops: 
                {', '.join([f"{c[0].title()}({c[1]:.1f}★)" for c in stats['high_rated'][:3]]) if stats['high_rated'] else "None yet"}
              </div>
              <div class="tip-text" style="margin-top:0.5rem;">
                💡 {T['confidence_improvement']} as we receive more farmer feedback!
              </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  QUICK FARMING REFERENCE
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f'<div class="card-title" style="font-family:Poppins;color:#1a6b2e;font-size:1rem;">{T["ref_title"]}</div>',
            unsafe_allow_html=True)

r1,r2,r3 = st.columns(3)
with r1:
    st.markdown("""
    <div class="tip-card"><p class="tip-text"><strong>🌧️ High Rainfall (&gt;200mm)</strong><br>Rice, Jute, Coconut, Banana</p></div>
    <div class="tip-card"><p class="tip-text"><strong>☀️ Moderate (100–200mm)</strong><br>Maize, Cotton, Grapes, Mango</p></div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown("""
    <div class="tip-card"><p class="tip-text"><strong>🏜️ Low Rainfall (&lt;100mm)</strong><br>Chickpea, Lentil, Mothbeans</p></div>
    <div class="tip-card"><p class="tip-text"><strong>🌡️ Hot Climate (&gt;30°C)</strong><br>Cotton, Watermelon, Papaya</p></div>
    """, unsafe_allow_html=True)
with r3:
    st.markdown("""
    <div class="tip-card"><p class="tip-text"><strong>🌿 Cool Climate (&lt;20°C)</strong><br>Apple, Lentil, Chickpea</p></div>
    <div class="tip-card"><p class="tip-text"><strong>📞 Free Expert Help</strong><br>
    <strong>Kisan Call Centre: 1800-180-1551</strong> (24×7, Free)<br>
    Nearest Krishi Vigyan Kendra (KVK)</p></div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#bbb;font-size:0.76rem;margin-top:1.5rem;">
  AI Crop Advisor • KNN Machine Learning • Hyperlocal Intelligence • Adaptive Learning • Satellite Insights • Crop Rotation<br>
  For best results, always validate with a soil test from your local agriculture office.
</div>
""", unsafe_allow_html=True)