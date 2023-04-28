import asyncio
import torch
import cv2

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging.logging import CsvLogging

dir = "/home/dionisius_baskoro/smart-ads"

MODEL = [{
        "weight" : f"{dir}/yolov5-6.0/crowdhuman6.0.pt",
        "yolo" : f"{dir}/yolov5-6.0/"
        },
        {
        "weight" : f"{dir}/yolov7/yolo7-crowdhuman.pt",
        "yolo" : f"{dir}/yolov7/"
        },
        {
        "weight" : f"{dir}/yolov7/yolo7tiny-crowdhuman.pt",
        "yolo" : f"{dir}/yolov7/"
        }]

class MyStorage (Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        self.consumer_servers = '10.184.0.4' # cloud kafka
        self.consumer_topic = ['cloud-input']
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyFogInference (Producer, CsvLogging):
    def __init__(self, consumer):
        self.consumer = consumer
        self.producer_topic = 'cloud-result'
        self.producer_servers = '10.184.0.4' # cloud kafka
        self.model = torch.hub.load(MODEL[0]["yolo"], 'custom', MODEL[0]["weight"],
                                    source='local', force_reload=True)
        CsvLogging.__init__(self)
        Producer.__init__(self)

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        # revert preprocess
        data = cv2.resize(data, None, fx=2, fy=2)

        # image inference
        self.model.classes = 1
        inference_results = self.model(data)

        # get inference result
        self.model.classes = 1
        inference_results = self.model(data)
        try:
            head = inference_results.pandas().xyxy[0].value_counts('name').sort_index()[0]
        except IndexError:
            head = 0

        try:
            person = inference_results.pandas().xyxy[0].value_counts('name').sort_index()[1]
        except IndexError:
            person = 0

        final_result = str({"head" : head, "person" : person})


        return final_result

    async def process(self, data):
        return await self._loop.run_in_executor(None,
                                               self._process,
                                               data)

    async def send(self, data):
        headers = self.message.headers
        await super().send(data, headers=headers)

async def main():
    _Consumer, _Producer = (MyStorage, MyFogInference)
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