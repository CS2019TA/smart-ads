FROM python:3.8.10
WORKDIR /code
COPY ./fog/jetson /code/fog/jetson
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python -m venv venv
COPY ./fogverse /code/fogverse
COPY ./setup.py /code/setup.py
COPY ./requirements.txt /code/requirements.txt
CMD ["source", "venv/bin/activate"]
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip3 install -e /code/.
CMD ["python3", "fog/jetson/cpu.py"]