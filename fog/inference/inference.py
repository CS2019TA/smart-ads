import asyncio
import torch
import psutil
import cv2
import csv
import datetime

from fogverse import Producer, Consumer, ConsumerStorage
from fogverse.logging.logging import CsvLogging

MODEL = [{
        "weight" : "yolov5-6.0/yolo5-crowdhuman.pt",
        "yolo" : "yolov5-6.0/"
        },
        {
        "weight" : "yolov7/yolo7-crowdhuman.pt",
        "yolo" : "yolov7/"
        },
        {
        "weight" : "yolov7/yolo7tiny-crowdhuman.pt",
        "yolo" : "yolov7/"
        }]

class MyStorage (Consumer, ConsumerStorage):
    def __init__(self, keep_messages=False):
        self.consumer_servers = '0.0.0.0'
        self.consumer_topic = 'input'
        Consumer.__init__(self)
        ConsumerStorage.__init__(self, keep_messages=keep_messages)

class MyFogInference (Producer, CsvLogging):
    def __init__(self, consumer):
        self.consumer = consumer
        self.producer_topic = 'fog-result'
        self.producer_servers = '0.0.0.0'
        self.counter = 0
        self.model = torch.hub.load(MODEL[0]["yolo"], 'custom', MODEL[0]["weight"],
                                    source='local', force_reload=True)
        CsvLogging.__init__(self)
        Producer.__init__(self)

        with open('inference_result.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "head", "person"])

    async def receive(self):
        return await self.consumer.get()

    def _process(self, data):
        cpu = psutil.cpu_percent()
        final_result = ''

        if (cpu < 60.0):
            self.counter = 0
            final_result = self.inference(data)

        elif (cpu < 80.0):
            if (self.counter % 2 == 0):
                self.producer_topic = 'forward'
                final_result = data
                self.counter += 1

            else:
                self.counter = 0
                final_result = self.inference(data)

        else :
            self.producer_topic = 'forward'
            self.counter = 0
            final_result = data

        return final_result

    def inference(self, data):
            final_result = ''
            self.producer_topic = 'fog-result'

            # revert preprocess
            data = cv2.resize(data, None, fx=2, fy=2)

            # image inference
            inference_results = self.model(data)

            # get inference result
            try:
                head = inference_results.pandas().xyxy[0].value_counts('name').sort_index()[0]
            except IndexError:
                head = 0

            try:
                person = inference_results.pandas().xyxy[0].value_counts('name').sort_index()[1]
            except IndexError:
                person = 0

            final_result = str({"head" : head, "person" : person})

            with open('inference_result.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)

                timestamp = datetime.datetime.now()
                data = [timestamp, head, person]
                writer.writerow(data)

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
    asyncio.run(main())