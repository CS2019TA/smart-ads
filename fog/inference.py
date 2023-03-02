import asyncio

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging.logging import CsvLogging
from fogverse.util import get_header, numpy_to_base64_url

class MyStorage (Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        self.consumer_servers = '192.168.1.18'
        self.consumer_topic = ['input','cpu-utilization']
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyProducer (Producer, CsvLogging):
    def __init__(self, consumer):
        self.consumer = consumer
        self.producer_topic = 'result'
        self.producer_servers = '192.168.1.18'
        CsvLogging.__init__(self)
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    # process your image here
    async def process(self, data):
        print(data)
        return data

    async def send(self, data):
        pass

async def main():
    _Consumer, _Producer = (MyStorage, MyProducer)
    consumer = _Consumer()
    producer = _Producer(consumer)
    tasks = [consumer.run(), producer.run()]

    try:
        await asyncio.gather(*tasks)
    except:
        for t in tasks:
            t.close()

if __name__ == '__main__':
    asyncio.run(main())