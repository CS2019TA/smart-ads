FROM fxdros/fogverse-smart-ads:inference

WORKDIR /app
COPY fog/jetson/inference/crowdhuman.pt .
COPY fog/jetson/inference/inference.py .
COPY fogverse/ fogverse/

CMD ["python3", "inference.py"]