FROM fxdros/fogverse-smart-ads:preprocess

WORKDIR /app
COPY input/producer.py .
COPY fogverse/ fogverse/
CMD ["python3", "producer.py"]