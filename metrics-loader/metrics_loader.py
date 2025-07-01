from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

def main():
    # Create SparkSession
    spark = SparkSession.builder \
        .appName("MetricsLoader") \
        .master("spark://spark:7077") \
        .config("spark.mongodb.input.uri", "mongodb://mongodb:27017/your_database.your_collection") \
        .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/your_database.your_collection") \
        .getOrCreate()

    # Read data from MongoDB
    mongo_df = spark.read \
        .format("mongo") \
        .option("uri", "mongodb://mongodb:27017/your_database.your_collection") \
        .load()

    # Perform aggregation (example: group by a field and count)
    aggregated_df = mongo_df.groupBy("your_field") \
        .agg(count("*").alias("count"))

    # Write aggregated data to PostgreSQL
    aggregated_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/superset") \
        .option("dbtable", "aggregated_table") \
        .option("user", "superset") \
        .option("password", "superset") \
        .mode("overwrite") \
        .save()

    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    main()