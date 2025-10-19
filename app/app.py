from flask import Flask, request, jsonify
from astropy.constants import M_sun, L_sun
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
    prediction = 10**(float(prediction[0])) / M_sun.value

    df = pd.read_csv("joined_out.csv")
    df = df.drop(columns=["met", "Teff", "R", "spectype"])
    df["M"] = 10**df["M"] / M_sun.value
    df["L"] = 10**df["L"] / L_sun.value

    label_df = pd.DataFrame({
        "Name": ["\N{GREEK SMALL LETTER ALPHA} Canis Majoris A",
                 "\N{GREEK SMALL LETTER ALPHA} Piscis Austrini",
                 "Sun",
                 "\N{GREEK SMALL LETTER ALPHA} Centauri C"],
        "L": [24.7, 16.63, 1,	0.001567],
        "M": [2.06, 1.92, 1, 0.1221],
        "Info": ["Also known as Sirius, the brighest star in the night sky",
                 "Was assumed to host the first exoplanet imaged at visible\nwavelengths; it later turned out to be a dust cloud",
                 "Centerpiece of our Solar System",
                 "Our closest extrasolar neighbor"]
    })

    return jsonify({
        "stars": df[["M", "L"]].to_dict(orient="records"),
        "labels": label_df.to_dict(orient="records"),
        "predicted": {"M": prediction, "L": luminosity }
        })