FROM fxdros/fogverse-smart-ads:preprocess

WORKDIR /app
COPY fog/jetson/preprocess/preprocess.py .
COPY fogverse/ fogverse/
CMD ["python3", "preprocess.py"]