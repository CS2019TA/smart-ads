import asyncio
import json

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging import CsvLogging

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self):
        self.consumer_servers = '10.5.95.175'
        self.consumer_topic = ['fog-result', 'cloud-result']
        Consumer.__init__(self)
        ConsumerStorage.__init__(self)

class MyAdsDecider(Producer, CsvLogging):
    def __init__(self, consumer, loop=None):
        self.consumer = consumer
        self.producer_servers = '10.5.95.175'
        CsvLogging.__init__(self)
        Producer.__init__(self, loop=loop)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        if (len(data) > 1):
            video = ''
            stripped_data = str(data).replace("\'", "\"")
            inference_dict = json.loads(stripped_data)
            if (inference_dict["head"] >= 1):
                video = '1'
            else :
                video = '0'

            return video

        return data

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

    async def send(self, data):
        self.producer_topic = self.message.topic
        headers = self.message.headers
        await super().send(data, headers=headers)

async def main():
    _Consumer, _Producer = (MyStorage, MyAdsDecider)
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