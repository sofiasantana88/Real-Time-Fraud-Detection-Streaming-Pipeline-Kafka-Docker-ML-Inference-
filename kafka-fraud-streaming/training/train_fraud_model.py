# train_fraud_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# ---- Step 1: load historical labeled data ----
df = pd.read_csv("historical_payments.csv")

features = [
    "amount",
    "country_risk_score",
    "failed_logins",
    "transaction_hour",
    "is_new_device"
]

X = df[features]
y = df["is_fraud"]   # 1 = fraud, 0 = normal

# ---- Step 2: train model ----
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# ---- Step 3: save model for streaming ----
joblib.dump(model, "fraud_model.pkl")

print("Model trained and saved as fraud_model.pkl")
