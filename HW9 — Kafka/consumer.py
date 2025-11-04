import json
from kafka import KafkaConsumer

received_orders = {}
received_payments = {}

print("Starting consumer... Waiting for messages...")

consumer = KafkaConsumer(
    'orders',
    'payments',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='order-processor-group',
    key_deserializer=bytes.decode,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

try:
    for message in consumer:
        order_id = message.key
        data = message.value

        if message.topic == 'orders':
            print(f"[RECEIVED ORDER] ID: {order_id}, Details: {data}")
            received_orders[order_id] = data

        elif message.topic == 'payments':
            print(f"[RECEIVED PAYMENT] ID: {order_id}, Details: {data}")
            received_payments[order_id] = data

        if order_id in received_orders and order_id in received_payments:
            print(f"\n✅ [COMPLETE] Order {order_id} fully received!")
            print(f"   Order Details: {received_orders[order_id]}")
            print(f"   Payment Details: {received_payments[order_id]}")
            print("--------------------------------------------------\n")

            del received_orders[order_id]
            del received_payments[order_id]

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
