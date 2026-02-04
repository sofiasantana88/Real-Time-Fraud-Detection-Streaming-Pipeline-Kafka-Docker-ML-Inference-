# fraud_consumer_kafka.py  (WITH CSV LOGGING)

import json
import joblib
from kafka import KafkaConsumer
import pandas as pd
import csv
import os
from datetime import datetime

# -------------------------------
# 1️⃣ Load model
# -------------------------------
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "fraud_model.pkl"
)

model = joblib.load(MODEL_PATH)

# -------------------------------
# 2️⃣ Prepare CSV log file
# -------------------------------
LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "outputs",
    "fraud_scores_stream.csv"
)

# If file does NOT exist, create it with headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "payment_id",
            "amount",
            "country_risk_score",
            "failed_logins",
            "transaction_hour",
            "is_new_device",
            "fraud_probability"
        ])

# -------------------------------
# 3️⃣ Connect to Kafka
# -------------------------------
consumer = KafkaConsumer(
    "test-payments",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",      # only new messages
    group_id="fraud_group",          # remember progress
    enable_auto_commit=True,         # normal production behavior
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Listening for payments...")

for message in consumer:
    try:
        payment_event = message.value  # <-- FIXED
        print(f"Received payment: {payment_event}")

        X = pd.DataFrame([[ 
            payment_event.get("amount", 0),
            payment_event.get("country_risk_score", 0),
            payment_event.get("failed_logins", 0),
            payment_event.get("transaction_hour", 0),
            payment_event.get("is_new_device", 0)
        ]], columns=model.feature_names_in_)

        fraud_prob = model.predict_proba(X)[0][1]
        print(f"Fraud risk score = {fraud_prob:.2f}\n")

        # (CSV logging stays the same)

    except Exception as e:
        print(f"Error processing message: {e}")
