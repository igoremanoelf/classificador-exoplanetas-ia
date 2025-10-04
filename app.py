# app.py

from flask import Flask, render_template, request
import joblib
import numpy as np

# DICTIONARY WITH EXPLANATORY LEGENDS
FEATURE_LEGENDS = {
    'koi_period': 'How often the star\'s "blink" (transit) occurs. This is the planet\'s "year".',
    'koi_duration': 'How long the star\'s light dims during each transit.',
    'koi_depth': 'How much the star\'s light dims. This is the main clue about the planet\'s size.',
    'koi_prad': 'The radius (size) of the planet, measured in "Earths". (e.g., 2.0 = twice the Earth\'s radius).',
    'koi_teq': 'The estimated average temperature on the planet\'s surface. Helps determine if it\'s in the "habitable zone".',
    'koi_insol': 'How much energy (light and heat) the planet receives from its star. A high value means it\'s being "toasted".',
    'koi_steff': 'The surface temperature of the star. Hotter (blue) and cooler (red) stars have different habitable zones.',
    'koi_slogg': 'The gravitational force on the star\'s surface. Helps confirm the star type.',
    'koi_srad': 'The size (radius) of the star. Essential for calculating the planet\'s actual size.',
    'koi_impact': 'Shows if the planet passed directly across the star\'s center (value ~0) or just grazed the edge (value ~1).',
    'koi_model_snr': 'The "clarity" or "sharpness" of the planet\'s signal. A high value means a strong, reliable signal.',
    'koi_fpflag_nt': 'NASA Flag: The shape of the "blink" does not look like a planetary transit.',
    'koi_fpflag_ss': 'NASA Flag: The event looks more like an eclipse between two stars.',
    'koi_fpflag_co': 'NASA Flag: The light source seems to shift, indicating contamination from a nearby star.',
    'koi_fpflag_ec': 'NASA Flag: The signal is "contaminated" by light from another nearby stellar event.'
}

app = Flask(__name__)

# Load the necessary artifacts
try:
    model = joblib.load('exoplanet_model.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    scaler = joblib.load('scaler.pkl')
    model_features = joblib.load('model_features.pkl')
    print("Model, encoder, scaler, and features loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: File '{e.filename}' not found. Run 'python train_model.py' first.")
    model = None

@app.route('/')
def home():
    if model is None:
        return "Error: The model has not been loaded. Check the server logs.", 500
    return render_template('index.html', features=model_features, legends=FEATURE_LEGENDS)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Error: Model not loaded.", 500

    try:
        input_dict = {feature: float(request.form.get(feature, 0)) for feature in model_features}
        input_values = [input_dict[feature] for feature in model_features]
        input_array = np.array(input_values).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        prediction_encoded = model.predict(input_scaled)
        prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
        
        return render_template('result.html', 
                               prediction=prediction_label, 
                               system_data=input_dict)

    except Exception as e:
        return f"An error occurred during prediction: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)
