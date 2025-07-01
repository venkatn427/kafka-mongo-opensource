FROM openjdk:8-jdk-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libpq-dev \
    gcc \
    build-essential \
    wget \
    && apt-get clean

# Install Spark
RUN wget https://archive.apache.org/dist/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz && \
    tar -xvzf spark-3.4.0-bin-hadoop3.tgz && \
    mv spark-3.4.0-bin-hadoop3 /opt/spark && \
    rm spark-3.4.0-bin-hadoop3.tgz

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install Python dependencies
RUN pip install pyspark pymongo psycopg2

# Copy the PySpark application
COPY metrics_loader.py /app/metrics_loader.py

CMD ["/opt/spark/bin/spark-submit", "--master", "local[*]", "/app/metrics_loader.py"]