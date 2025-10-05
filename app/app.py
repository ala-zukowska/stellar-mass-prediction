from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="frontend/dist", static_url_path="/")

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    luminosity = data.get("luminosity")
    metallicity = data.get("metallicity")

    if luminosity is None or metallicity is None:
        return jsonify({"error": "Missing parameters"}), 400

    # Add linear regression model later
    prediction = float(luminosity) * float(metallicity)
    return jsonify({"prediction": prediction})