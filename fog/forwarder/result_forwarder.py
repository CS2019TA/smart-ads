import asyncio

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging import CsvLogging


class MyStorage(Consumer, ConsumerStorage):
    def __init__(self):
        self.consumer_servers = '0.0.0.0'  # cloud kafka ip address
        self.consumer_topic = 'cloud-result'
        Consumer.__init__(self)
        ConsumerStorage.__init__(self)


class MyResultForwarder(Producer, CsvLogging):
    def __init__(self, consumer, loop=None):
        self.consumer = consumer
        self.producer_servers = '0.0.0.0'  # fog kafka ip address
        CsvLogging.__init__(self)
        Producer.__init__(self, loop=loop)

    async def receive(self):
        return await self.consumer.get()

    async def send(self, data):
        self.producer_topic = self.message.topic
        headers = self.message.headers
        await super().send(data, headers=headers)


async def main():
    _Consumer, _Producer = (MyStorage, MyResultForwarder)
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
