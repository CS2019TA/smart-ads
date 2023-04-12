from fastapi import APIRouter
from aiokafka import AIOKafkaConsumer
import asyncio

KAFKA_BOOTSTRAP_SERVERS= "10.5.95.175:9092"
KAFKA_TOPIC= ["fog-result", "cloud-result"]
KAFKA_CONSUMER_GROUP= "client"

loop = asyncio.get_event_loop()
route = APIRouter()

data = {}

@route.get("/consume")
async def show_data():
    return (data)

async def consume():
    global data
    consumer = AIOKafkaConsumer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    consumer.subscribe(KAFKA_TOPIC)
    await consumer.start()
    try:
        async for msg in consumer:
            data["ads"] = str(msg.value)[2:3]
            data["timestamp"] = msg.headers[1][1].decode('utf-8')
            data["topic"] = str(msg.topic)

    finally:
        await consumer.stop()