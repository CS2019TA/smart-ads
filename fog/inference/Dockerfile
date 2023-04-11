FROM fxdros/fogverse-smart-ads:inference

WORKDIR /app
COPY yolov5-6.0/ yolov5-6.0/
COPY fog/inference/inference.py .
COPY fogverse/ fogverse/

CMD ["python3", "inference.py"]