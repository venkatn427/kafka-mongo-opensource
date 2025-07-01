FROM bitnami/spark:latest

WORKDIR /app

# Install Python dependencies
RUN pip install pyspark pymongo psycopg2

# Copy the PySpark application
COPY metrics_loader.py /app/metrics_loader.py

CMD ["/opt/spark/bin/spark-submit", "--master", "spark://spark:7077", "/app/metrics_loader.py"]