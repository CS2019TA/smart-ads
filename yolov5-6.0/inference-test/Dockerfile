FROM fxdros/fogverse-smart-ads:inference

WORKDIR /app
COPY yolov5-6.0/ yolov5-6.0/

CMD ["python3", "yolov5-6.0/detect.py", "--weights", "yolov5-6.0/crowdhuman6.0.pt"]