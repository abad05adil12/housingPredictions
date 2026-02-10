from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import sqlite3

app = Flask(__name__)
CORS(app)  

model = pickle.load(open("house_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
le = pickle.load(open("location_encoder.pkl", "rb"))

def create_db():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            size REAL,
            bedrooms INTEGER,
            age INTEGER,
            location TEXT,
            predicted_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

create_db()

@app.route("/")
def home():
    return "House Price Prediction API is running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        size = float(data["Size_sqft"])
        bedrooms = int(data["Bedrooms"])
        age = int(data["House_Age"])
        location = str(data["Location"])

        location_encoded = le.transform([location])[0]
        features = np.array([[size, bedrooms, age, location_encoded]])
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]

        conn = sqlite3.connect("predictions.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO history(size, bedrooms, age, location, predicted_price)
            VALUES (?, ?, ?, ?, ?)
        """, (size, bedrooms, age, location, prediction))
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "predicted_price_rupees": round(float(prediction), 2)
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/history", methods=["GET"])
def history():
    try:
        conn = sqlite3.connect("predictions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        history_list = []
        for r in rows:
            history_list.append({
                "id": r[0],
                "size": r[1],
                "bedrooms": r[2],
                "age": r[3],
                "location": r[4],
                "predicted_price": r[5],
                "timestamp": r[6]
            })

        return jsonify({"success": True, "history": history_list})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)