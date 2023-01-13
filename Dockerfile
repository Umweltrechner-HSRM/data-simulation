FROM python:3.10.5-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY data data
COPY src src
COPY logs logs
COPY buffer buffer

CMD ["python", "./src/sensor_data_generator.py"]