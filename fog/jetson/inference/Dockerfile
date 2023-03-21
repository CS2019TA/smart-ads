FROM fxdros/fogverse-smart-ads:inference

WORKDIR /app
COPY fog/jetson/inference/inference.py .
COPY fogverse/ fogverse/
COPY yolov5/ yolov5/
CMD ["python3", "inference.py"]