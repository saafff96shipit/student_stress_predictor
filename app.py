from flask import Flask, request, render_template_string
import pickle

app = Flask(__name__)

# Load trained model
model = pickle.load(open("stress_model.pkl", "rb"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Stress Prediction System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #74ebd5, #ACB6E5);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: white;
            padding: 30px;
            width: 450px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 6px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: none;
            background: #333;
            color: white;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background: #555;
        }

        .result-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            background: #f4f4f4;
            text-align: center;
        }

        .meter {
            height: 20px;
            border-radius: 10px;
            background: #ddd;
            margin: 10px 0;
        }

        .meter-fill {
            height: 100%;
            border-radius: 10px;
        }

        .low { background: #2ecc71; }
        .medium { background: #f39c12; }
        .high { background: #e74c3c; }

        footer {
            text-align: center;
            font-size: 12px;
            margin-top: 15px;
            color: gray;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Student Stress Prediction</h1>

    <form method="POST" action="/predict">
        <input type="number" name="sleep" placeholder="Sleep Hours" required>
        <input type="number" name="study" placeholder="Study Hours" required>
        <input type="number" name="screen" placeholder="Screen Time (Hours)" required>
        <input type="number" name="social" placeholder="Social Activity Level (1-5)" required>
        <button type="submit">Predict Stress Level</button>
    </form>

    {% if level %}
    <div class="result-box">
        <h2>Stress Prediction Result</h2>

        <div class="meter">
            <div class="meter-fill {{ meter_class }}" style="width: {{ score }}%;"></div>
        </div>

        <h3>Stress Level: {{ level }}</h3>
        <h4>Stress Score: {{ score }}%</h4>
        <p>{{ guidance }}</p>
    </div>
    {% endif %}

    <footer>
        Intelligent Guidance System | ML-Based Prediction Model
    </footer>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/predict", methods=["POST"])
def predict():
    sleep = int(request.form["sleep"])
    study = int(request.form["study"])
    screen = int(request.form["screen"])
    social = int(request.form["social"])

    prediction = model.predict([[sleep, study, screen, social]])[0]

    if prediction == 0:
        level = "LOW ✅"
        score = 25
        guidance = "You are maintaining a healthy balance. Continue regular sleep and social interaction."
        meter_class = "low"

    elif prediction == 1:
        level = "MODERATE ⚠"
        score = 60
        guidance = "Try improving sleep schedule, reducing screen time, and planning study hours efficiently."
        meter_class = "medium"

    else:
        level = "HIGH ❗"
        score = 85
        guidance = "Immediate stress management required. Practice relaxation techniques and seek guidance."
        meter_class = "high"

    return render_template_string(
        HTML_TEMPLATE,
        level=level,
        score=score,
        guidance=guidance,
        meter_class=meter_class
    )
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))