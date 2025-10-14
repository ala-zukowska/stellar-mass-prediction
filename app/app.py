from flask import Flask, request, jsonify
import joblib
import pandas as pd
import math

app = Flask(__name__, static_folder="frontend/dist", static_url_path="/")

model = joblib.load("linear_model.pkl")

@app.route("/", methods=["GET"])
@app.route("/predict", methods=["GET"])
@app.route("/graphs", methods=["GET"])
@app.route("/definitions", methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    luminosity = data.get("luminosity")
    metallicity = data.get("metallicity")
    if luminosity is None or metallicity is None:
        return jsonify({"error": "Missing parameters"}), 400
    # The model expects the luminosity in log watts
    log_watts = 26.583 + math.log10(luminosity)
    X_new = pd.DataFrame([[log_watts, metallicity]], columns=["L", "met"])
    prediction = model.predict(X_new)

    return jsonify({"prediction": float(prediction[0])})