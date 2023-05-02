import asyncio
import json
import time

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
            message = json.loads(msg.value.decode("utf-8").replace("\'", "\""))
            data["ads"] = message["video"]
            data["topic"] = message["topic"]
            data["timestamp"] = msg.headers[1][1].decode('utf-8')

    finally:
        await consumer.stop()