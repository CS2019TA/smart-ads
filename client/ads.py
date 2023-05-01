import asyncio
import json

from csv import writer
from datetime import datetime, date, timedelta
from fastapi import APIRouter
from aiokafka import AIOKafkaConsumer

KAFKA_BOOTSTRAP_SERVERS= "192.168.1.3"
KAFKA_TOPIC= "ads"
KAFKA_CONSUMER_GROUP= "client"

loop = asyncio.get_event_loop()
route = APIRouter()

data = {}

@route.get("/consume")
async def show_data():
    return (data)

async def consume():
    global data
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            time_delay = ''
            message = json.loads(msg.value.decode("utf-8").replace("\'", "\""))
            data["ads"] = message["video"]
            data["topic"] = message["topic"]
            data["timestamp"] = msg.headers[1][1].decode('utf-8')

            format_string = "%Y-%m-%d %H:%M:%S.%f"
            message_timestamp = datetime.strptime(data["timestamp"], format_string)
            message_timestamp = message_timestamp + timedelta(hours=6, minutes=59, seconds=59)
            current_dateTime = datetime.now()

            time_delay = current_dateTime - message_timestamp
            data["latency"] = time_delay

            with open('log_latency.csv', 'a') as f:
                writer_object = writer(f)
                writer_object.writerow([time_delay])
                f.close()

    finally:
        await consumer.stop()