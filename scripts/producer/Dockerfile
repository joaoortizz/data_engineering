FROM python:3.8.10-slim

# Install pip requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /
COPY . /

CMD ["python3", "producer.py"]