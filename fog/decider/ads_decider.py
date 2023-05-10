import asyncio
import json

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging import CsvLogging

class MyStorage(Consumer, ConsumerStorage):
    def __init__(self):
        self.consumer_servers = '192.168.1.19'
        self.consumer_topic = ['fog-result', 'cloud-result']
        Consumer.__init__(self)
        ConsumerStorage.__init__(self)

class MyAdsDecider(Producer, CsvLogging):
    def __init__(self, consumer, loop=None):
        self.consumer = consumer
        self.producer_topic = "ads"
        self.producer_servers = '192.168.1.19'
        CsvLogging.__init__(self)
        Producer.__init__(self, loop=loop)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        # prevent false data read
        if (data[2:7] != "topic"):
            advertisement = {}
            advertisement["topic"] = self.message.topic

            stripped_data = str(data).replace("\'", "\"")
            inference_dict = json.loads(stripped_data)

            if (inference_dict["head"] >= 10 or inference_dict["person"] >= 10):
                advertisement["video"] = '2'
            elif (inference_dict["head"] >= 5 or inference_dict["person"] >= 5):
                advertisement["video"] = '1'
            else :
                advertisement["video"] = '0'

            return str(advertisement)

        return data

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

    async def send(self, data):
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