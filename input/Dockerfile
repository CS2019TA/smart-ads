FROM python
WORKDIR /code
COPY producer.py /code/
COPY ../requirements.txt /code/requirements.txt
RUN python -m venv venv
CMD ["source", "venv/bin/activate"]
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip3 install -e ../.
CMD ["python3", "producer.py"]
