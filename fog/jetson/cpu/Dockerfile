FROM fxdros/fogverse-smart-ads:cpu-check

WORKDIR /app
COPY fog/jetson/cpu/cpu.py .
COPY fogverse/ fogverse/
CMD ["python3", "cpu.py"]