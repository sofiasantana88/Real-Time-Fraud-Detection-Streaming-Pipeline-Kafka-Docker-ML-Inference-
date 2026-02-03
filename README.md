# Real-Time-Fraud-Detection-Streaming-Pipeline-Kafka-Docker-ML-Inference-

A real-time data streaming project that simulates payment events, streams them through Apache Kafka, and performs live fraud-risk scoring using a trained machine learning model. The scored results are written to a CSV sink for downstream analysis.

This project demonstrates core **data engineering concepts** including streaming ingestion, message-based decoupling, and real-time processing.

---

## Architecture Overview

**Producer (Python)** ➜ **Kafka Topic (`test-payments`)** ➜ **Consumer / Stream Processor (Python)** ➜ **CSV Sink**

- The **producer** generates a payment event every 3 seconds.
- **Apache Kafka** acts as the streaming backbone.
- The **consumer** performs:
  - JSON deserialization
  - feature extraction
  - fraud probability inference
  - streaming output logging

---

## Tech Stack

- Docker & Docker Compose
- Apache Kafka + Zookeeper
- Python
  - kafka-python
  - pandas
  - scikit-learn
  - joblib

---

## Payment Event Schema

Each Kafka message follows this structure:

```json
{
  "payment_id": 1,
  "amount": 1200,
  "country_risk_score": 0.68,
  "failed_logins": 3,
  "transaction_hour": 18,
  "is_new_device": 1
}
Project Structure
kafka-fraud-streaming/
├── docker-compose.yml
├── README.md
├── data/
│   └── historical_payments.csv
├── models/
│   └── fraud_model.pkl
├── outputs/
│   └── fraud_scores_stream.csv
├── scripts/
│   └── launch_project.ps1
├── streaming/
│   ├── producer.py
│   └── consumer.py
└── training/
    └── train_fraud_model.py

How to Run the Pipeline
1) Start Kafka
From the project root:

docker compose up -d
docker ps
2) Train the model (optional)
If the model file already exists, this step can be skipped.

py .\training\train_fraud_model.py
3) Start the consumer (stream processor)
py .\streaming\consumer.py
4) Start the producer (in a second terminal)
py .\streaming\producer.py
You should see payment events produced every 3 seconds and fraud scores printed in real time.

Output
Fraud scores are appended to:

outputs/fraud_scores_stream.csv
This file can be used for downstream analytics or visualization.

Kafka Offset Behavior
The consumer is configured with:

auto_offset_reset="latest"

a stable consumer group

This ensures only new real-time events are processed, mimicking production streaming behavior.

One-Click Launcher (Windows)
The pipeline can be started end-to-end using a PowerShell launcher script:

.\scripts\launch_project.ps1
This script automatically starts Kafka, the consumer, and the producer.

Future Improvements
Persist fraud scores to a database (Postgres / SQLite)

Publish scored events to a second Kafka topic

Add schema validation for streaming messages

Fully containerize producer and consumer services
