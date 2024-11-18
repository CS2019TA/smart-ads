from flask import Flask, Response, render_template
from flask_socketio import SocketIO
from confluent_kafka import Consumer
from flask_cors import CORS

import threading
import json

app = Flask(__name__)
CORS(app)

KAFKA_BROKER = '0.0.0.0:9092'
KAFKA_TOPIC = 'ads'

data = {}

# Kafka Consumer: Fetch messages from Kafka and send them to WebSocket clients
def kafka_consumer():
    global data
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'websocket_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([KAFKA_TOPIC])

    while True:
        msg = consumer.poll(1.0)  # Poll with a timeout of 1 second
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Emit Kafka message to WebSocket clients
        message =  json.loads(msg.value().decode("utf-8").replace("\'", "\""))
        data["ads"] = message["video"]
        data["topic"] = message["topic"]
        data["timestamp"] = msg.headers()[1][1].decode('utf-8')

# Flask route
@app.route('/stream')
def stream():
    return (data)

@app.route('/')
def index():
    return render_template('index.html')

# Start Kafka Consumer thread
if __name__ == '__main__':
    threading.Thread(target=kafka_consumer, daemon=True).start()
    app.run(port=5000, debug=True)
