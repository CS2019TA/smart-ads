import asyncio

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging import CsvLogging

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self):
        self.consumer_servers = '192.168.1.5'
        self.consumer_topic = ['input', 'cpu-utilization']
        Consumer.__init__(self)
        ConsumerStorage.__init__(self)

class DeviceDecider (Producer, CsvLogging):
    def __init__(self, consumer, loop=None):
        self.consumer = consumer
        self.producer_topic = 'fog-input'
        self.producer_servers = '192.168.1.5'
        self.forwarded_data = ''
        CsvLogging.__init__(self)
        Producer.__init__(self, loop=loop)

    async def receive(self):
        return await self.consumer.get()

    async def process(self, data):
        message_topic = self.message.topic
        if (message_topic == 'cpu-utilization'):
            if (float(data) > 70.0):
                self.producer_topic = 'preprocess'
            else:
                self.producer_topic = 'fog-input'
        else:
            self.forwarded_data = data
        return (self.forwarded_data)

    async def send(self, data):
        await super().send(data)

async def main():
    _Consumer, _Producer = (MyStorage, DeviceDecider)
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