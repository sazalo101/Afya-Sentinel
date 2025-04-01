from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.core.credentials import AzureKeyCredential
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# ======================
# DUMMY DATA GENERATION
# ======================

def generate_kenyan_hospital_data():
    counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kakamega"]
    data = []
    for county in counties:
        for day in range(30):  # Last 30 days
            date = (datetime.now() - timedelta(days=30-day)).strftime("%Y-%m-%d")
            data.append({
                "county": county,
                "date": date,
                "beds_available": random.randint(20, 150),
                "icu_capacity": random.randint(5, 30),
                "staff_shortage": random.randint(0, 15),
                "malaria_cases": random.randint(10, 200),
                "cholera_cases": random.randint(0, 10),
                "disease_alerts": random.randint(0, 50)
            })
    return pd.DataFrame(data)

# Initialize dummy data
df = generate_kenyan_hospital_data()

# ======================
# AZURE AI SERVICES
# ======================

# Initialize clients (use your Azure keys)
text_analytics_client = TextAnalyticsClient(
    endpoint="https://kenya-health-text.cognitiveservices.azure.com/",
    credential=AzureKeyCredential("AZURE_TEXT_KEY")
)

anomaly_detector = AnomalyDetectorClient(
    endpoint="https://kenya-anomaly-detector.cognitiveservices.azure.com/",
    credential=AzureKeyCredential("AZURE_ANOMALY_KEY")
)

def detect_health_crisis(county_data):
    """Use Azure Anomaly Detector to find unusual patterns"""
    series = [{"timestamp": row["date"], "value": row["malaria_cases"]} for _, row in county_data.iterrows()]
    request = {"series": series, "granularity": "daily"}
    response = anomaly_detector.detect_entire_series(request)
    return any([point.is_anomaly for point in response.is_anomaly])

def analyze_social_sentiment(texts):
    """Use Azure Text Analytics for Swahili/English sentiment"""
    response = text_analytics_client.analyze_sentiment(documents=texts)
    return [doc.sentiment for doc in response]

# ======================
# PREDICTION ENGINE
# ======================

def calculate_risk_score(county_data):
    """Composite risk score using multiple factors"""
    beds_risk = 0.4 * (1 - (county_data["beds_available"].iloc[-1] / 150))
    disease_risk = 0.3 * (county_data["malaria_cases"].iloc[-1] / 200)
    anomaly_risk = 0.3 if detect_health_crisis(county_data) else 0
    return min(1.0, beds_risk + disease_risk + anomaly_risk) * 100

def generate_recommendations(county, risk_score):
    """Dynamic recommendations based on risk"""
    recommendations = []
    
    if risk_score > 70:
        recommendations.append({
            "icon": "🚨",
            "title": "Emergency Protocol Activation",
            "description": "Activate county emergency response team per Kenya MOH guidelines"
        })
        recommendations.append({
            "icon": "💉",
            "title": "Request Medical Supplies",
            "description": f"Order emergency stock from KEMSA for {county}"
        })
    
    if risk_score > 50:
        recommendations.append({
            "icon": "📢",
            "title": "Public Health Alert",
            "description": "Issue SMS alerts via Kenya MOH bulk messaging system"
        })
    
    if not recommendations:
        recommendations.append({
            "icon": "✅",
            "title": "Stable Situation",
            "description": "Continue routine monitoring per county health plan"
        })
    
    return recommendations

# ======================
# FLASK ROUTES
# ======================

@app.route("/")
def dashboard():
    counties = df["county"].unique()
    latest_data = df.groupby("county").last().reset_index()
    return render_template("index.html", counties=counties, latest_data=latest_data)

@app.route("/predict/<county>")
def predict(county):
    county_data = df[df["county"] == county]
    risk_score = calculate_risk_score(county_data)
    recommendations = generate_recommendations(county, risk_score)
    
    # Generate trend data for charts
    trend_dates = county_data["date"].tolist()
    trend_beds = county_data["beds_available"].tolist()
    trend_cases = county_data["malaria_cases"].tolist()
    
    return render_template("predict.html",
        county=county,
        risk_score=risk_score,
        recommendations=recommendations,
        trend_dates=trend_dates,
        trend_beds=trend_beds,
        trend_cases=trend_cases,
        latest=county_data.iloc[-1].to_dict()
    )

@app.route("/api/predict/<county>", methods=["GET"])
def api_predict(county):
    county_data = df[df["county"] == county]
    risk_score = calculate_risk_score(county_data)
    return jsonify({
        "county": county,
        "risk_score": risk_score,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True)