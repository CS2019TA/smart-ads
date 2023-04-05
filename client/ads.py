from fastapi import APIRouter
from aiokafka import AIOKafkaConsumer
import asyncio

KAFKA_BOOTSTRAP_SERVERS= "192.168.1.6:9092"
KAFKA_TOPIC="ads"
KAFKA_CONSUMER_GROUP="group-id"

loop = asyncio.get_event_loop()
route = APIRouter()

data = {}

@route.get("/consume")
async def show_data():
    return (data)

async def consume():
    global data
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            data["ads"] = str(msg.value)[2:3]
            data["timestamp"] = msg.headers[1][1].decode('utf-8')

    finally:
        await consumer.stop()