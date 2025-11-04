import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    key_serializer=str.encode,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting producer...")

for i in range(10):
    order_id = f"ORD-{100 + i}"

    order_data = {
        'item': f'Item {i}',
        'quantity': random.randint(1, 5)
    }

    payment_data = {
        'amount': random.randint(100, 1000),
        'currency': 'RUB'
    }

    try:
        producer.send('orders', key=order_id, value=order_data)
        print(f"Sent ORDER with ID: {order_id}")

        time.sleep(random.uniform(0.1, 0.5))

        producer.send('payments', key=order_id, value=payment_data)
        print(f"Sent PAYMENT with ID: {order_id}")

        time.sleep(1)

    except Exception as e:
        print(f"Error while sending: {e}")

print("All messages sent. Shutting down...")
producer.flush()
producer.close()
