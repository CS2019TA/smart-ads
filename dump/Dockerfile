FROM arm64v8/python:3.8-alpine3.16

WORKDIR /code

COPY ./requirements.txt requirements.txt
COPY ./setup.py setup.py
COPY ./fogverse fogverse
COPY fog/jetson/cpu/cpu.py cpu.py

RUN pip install -e .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD [ "python", "cpu.py" ]