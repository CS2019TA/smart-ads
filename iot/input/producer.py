import asyncio
import cv2

from fogverse import ConsumerStorage, Producer, OpenCVConsumer
from fogverse.logging import CsvLogging
from fogverse.util import get_timestamp_str, get_cam_id

class MyStorage(OpenCVConsumer, ConsumerStorage):
    def __init__(self):
        OpenCVConsumer.__init__(self)
        ConsumerStorage.__init__(self)
        self.consumer.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
        self.consumer.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.consumer.set(cv2.CAP_PROP_FPS, 5)

class ProducerTemplates(CsvLogging, Producer):
    def __init__(self, consumer, loop=None):
        self.consumer = consumer
        self.producer_topic = 'input'
        self.cam_id = get_cam_id()
        self.frame_idx = 1
        CsvLogging.__init__(self)
        Producer.__init__(self, loop=loop)

    async def receive(self):
        return await self.consumer.get()

    def _process(self,data):
        img_resized = cv2.resize(data, (480,640))
        return cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

    async def send(self, data):
        key = str(self.frame_idx).encode()
        headers = [
            ('frame_idx', str(self.frame_idx).encode()),
            ('timestamp', get_timestamp_str().encode())]
        await super().send(data, key=key, headers=headers)
        self.frame_idx += 1

class MyProducer(ProducerTemplates):
    def __init__(self, consumer, loop=None):
        self.producer_servers = '192.168.1.17'
        super().__init__(consumer, loop)

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
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()