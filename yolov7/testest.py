import torch
import os
import time
from datetime import timedelta

model = torch.hub.load('D:\File-Ngoding\TA\yolov7', 'custom',
                       'D:\File-Ngoding\TA\yolov7\weights\crowdhuman.pt', source='local')
# model = torch.hub.load('WongKinYiu/yolov7', 'custom',
#                        'D:\File-Ngoding\TA\yolov7\weights\crowdhuman.pt')
dir = 'D:\File-Ngoding\TA\yolov7\inference\images\\test'
files = list(map(lambda x: os.path.join(
    os.path.abspath(dir), x), os.listdir(dir)))

# Inference
start_time = time.monotonic()
results = model(dir+"\\10_11kepala.jpg")
end_time = time.monotonic()
results.print()
# results.save()
print('Inference Time')
print(timedelta(seconds=(end_time - start_time)))
# print(results.pandas().xyxy[0])
