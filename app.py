from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Cargar modelo
with open('modelo_ransomware_rf_balanceado.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/')
def home():
    return jsonify({"message": "API Detección Ransomware Activa"})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": True})


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = data['features']

        # Validar que tenemos 15 características
        if len(features) != 15:
            return jsonify({"error": f"Se esperaban 15 características, se recibieron {len(features)}"}), 400

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]

        return jsonify({
            "prediction": int(prediction),
            "confidence": float(np.max(probability)),
            "class": "BENIGN" if prediction == 1 else "RANSOMWARE"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
