from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    age = float(request.form["age"])
    weight = float(request.form["weight"])
    cycle = float(request.form["cycle"])
    acne = int(request.form["acne"])
    hair = int(request.form["hair"])

    # BMI
    bmi = weight / (1.6 ** 2)

    # ML conversion
    hcg1 = (cycle * 20) + acne * 500
    hcg2 = (bmi * 50) + hair * 500
    amh = (age / 2) + acne * 2 + hair * 2

    final = np.array([[hcg1, hcg2, amh]])

    prediction = model.predict(final)

    # Risk score
    risk_score = 0
    if cycle > 35: risk_score += 25
    if acne == 1: risk_score += 20
    if hair == 1: risk_score += 20
    if bmi > 25: risk_score += 35

    risk_percent = min(risk_score, 100)

    # 🔥 PRO Risk Levels (INSIDE function)
    if risk_percent < 30:
        result = "Low Risk"
        color = "green"
    elif risk_percent < 70:
        result = "Medium Risk"
        color = "orange"
    else:
        result = "High Risk"
        color = "red"

    # PCOS / PCOD classification
    if cycle > 40 and acne == 1 and hair == 1 and bmi > 27:
        condition = "PCOS"
    elif cycle > 35 and (acne == 1 or hair == 1):
        condition = "PCOD"
    else:
        condition = "Normal"

    # Tips
    if condition == "PCOS":
        tip = "Consult doctor, strict diet, regular exercise."
    elif condition == "PCOD":
        tip = "Improve lifestyle, balanced diet, workout."
    else:
        tip = "Maintain healthy lifestyle."

    # 📄 Health Report
    report = f"""
Age: {age}
BMI: {round(bmi,2)}
Cycle Length: {cycle}
Condition: {condition}
Risk Score: {risk_percent}%
"""

    return render_template(
        "result.html",
        result=result,
        color=color,
        risk=risk_percent,
        condition=condition,
        tip=tip,
        report=report
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)