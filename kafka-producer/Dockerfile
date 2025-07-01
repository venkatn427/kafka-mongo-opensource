FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py /app/producer.py

CMD ["python", "/app/producer.py"]