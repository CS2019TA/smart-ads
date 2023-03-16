FROM fxdros/fogverse-smart-ads:inference

WORKDIR /app
COPY fog/jetson/inference/cpu.py .
COPY fogverse/ fogverse/
CMD ["python3", "inference.py"]