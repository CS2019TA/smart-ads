FROM fxdros/fogverse-smart-ads:base-image-cpu

WORKDIR /app
COPY fog/raspberry/preprocess.py .
COPY fogverse/ fogverse/
CMD ["python3", "preprocess.py"]