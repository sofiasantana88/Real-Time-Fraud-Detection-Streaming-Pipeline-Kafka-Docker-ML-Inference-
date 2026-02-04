import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import random

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "test-payments"
RETRY_WAIT = 5
SEND_INTERVAL = 3

# -------------------------------
# 1️⃣ Wait for Kafka to be ready
# -------------------------------
print("⏳ Waiting for Kafka broker to become ready...")

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
            retry_backoff_ms=1000,
            request_timeout_ms=30000,
            api_version_auto_timeout_ms=30000
        )
        
        # ✅ Check metadata instead of sending a None message
        producer.partitions_for(TOPIC)
        print("✅ Kafka broker is ready!")
        break

    except NoBrokersAvailable:
        print(f"⚠️ Kafka not ready, retrying in {RETRY_WAIT}s...")
        time.sleep(RETRY_WAIT)

# -------------------------------
# 2️⃣ Auto-produce payment events
# -------------------------------
payment_id = 1
print(f"🚀 Auto producer started. Sending payment every {SEND_INTERVAL} seconds...")

try:
    while True:
        payment_event = {
            "payment_id": payment_id,
            "amount": random.choice([200, 500, 900, 1200, 1800, 2500]),
            "country_risk_score": round(random.uniform(0.1, 1.0), 2),
            "failed_logins": random.randint(0, 6),
            "transaction_hour": random.randint(0, 23),
            "is_new_device": random.choice([0, 1])
        }

        producer.send(TOPIC, payment_event)
        print(f"📤 Sent payment event: {payment_event}")

        payment_id += 1
        time.sleep(SEND_INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 Stopping producer...")
finally:
    producer.flush()
    producer.close()
    print("✅ Producer closed cleanly.")



# # auto_producer_kafka.py
# import json
# import time
# import random
# from kafka import KafkaProducer

# # producer = KafkaProducer(
# #     bootstrap_servers="localhost:9092",
# #     value_serializer=lambda v: json.dumps(v).encode("utf-8")
# # )

# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     retries=10,
#     retry_backoff_ms=1000,
#     request_timeout_ms=30000,
#     api_version_auto_timeout_ms=30000
# )

# print("🚀 Auto producer started. Sending payment every 3 seconds...\n")

# payment_id = 1

# while True:
#     payment_event = {
#         "payment_id": payment_id,
#         "amount": random.choice([200, 500, 900, 1200, 1800, 2500]),
#         "country_risk_score": round(random.uniform(0.1, 1.0), 2),
#         "failed_logins": random.randint(0, 6),
#         "transaction_hour": random.randint(0, 23),
#         "is_new_device": random.choice([0, 1])
#     }

#     producer.send("test-payments", payment_event)
#     print(f"📤 Sent: {payment_event}")

#     payment_id += 1
#     time.sleep(3)   # wait 3 seconds before next payment
