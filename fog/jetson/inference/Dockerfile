FROM fxdros/fogverse-smart-ads:inference

RUN pip3 install --upgrade pip \
    opencv-python

RUN pip3 install numpy \
    matplotlib \
    Pillow \
    PyYAML \
    requests \
    scipy \
    thop \
    torchvision \
    tqdm \
    tensorboard \
    seaborn

WORKDIR /app
COPY fog/jetson/inference/crowdhuman.pt .
COPY fog/jetson/inference/inference.py .
COPY fogverse/ fogverse/

CMD ["python3", "inference.py"]