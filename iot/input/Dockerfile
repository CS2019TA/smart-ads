FROM fxdros/fogverse-smart-ads:preprocess

WORKDIR /app
COPY iot/input/producer.py .
COPY fogverse/ fogverse/
CMD ["python3", "producer.py"]