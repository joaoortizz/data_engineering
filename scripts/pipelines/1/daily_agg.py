from pyspark.sql import SparkSession
from pyspark.sql import functions as F

import uuid
import configparser

config = configparser.ConfigParser()
config.read('./pipelines/config.ini')

MONGODB_URL = config['MONGODB']['URL']
KAFKA_SERVERS = f"{config['KAFKA_BROKER']['BootstrapServer']}:{config['KAFKA_BROKER']['BootstrapServerPort']}"
MASTER = config['SPARK']['Master']
APP_NAME = '1_daily_agg'

if __name__ == '__main__':
    @F.udf
    def create_uuid(string_base):
        """
            Generate a unique identifier based on a string
            parameter:
            - string_base: string
            return:
            - uuid: string
        """
        return str(uuid.uuid3(uuid.NAMESPACE_DNS,string_base))

    spark = SparkSession.builder \
        .master(MASTER) \
        .appName(APP_NAME) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector:10.0.0") \
        .getOrCreate()

    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_SERVERS) \
        .option("subscribe", "init") \
        .load()

    df = df.withColumn('value_str', df['value'].cast('string')).drop('value')

    schema = spark.read.json(df.rdd.map(lambda row: row.value_str)).schema

    df = df.withColumn("jsonData", F.from_json(F.col("value_str"), schema)) \
        .select("jsonData.*") \
        .withColumn("datetime", (F.col("time")).cast("timestamp")) \
        .withColumn("date_part", F.to_date(F.col("datetime"))) \
        .select("*", F.regexp_replace(F.col("date_part").cast("string"), "-", "").cast("int").alias("date")) \
        .drop('time') \
        .drop('datetime') \
        .drop('date_part') \
        .groupBy("date", "country", "platform") \
        .count() \
        .sort(F.col("count").desc())

    df = df.withColumn('Unique_Name', F.concat("date","country", "platform")) \
        .withColumn("_id",create_uuid('Unique_Name')) \
        .drop('Unique_Name')

    df.show(truncate=False)

    df.write \
        .format("mongodb") \
        .option("daily_aggregation", "collNameToUpdate").mode("append") \
        .option("replaceDocument", "false") \
        .option('spark.mongodb.connection.uri', MONGODB_URL) \
        .option('spark.mongodb.database', 'events') \
        .option('spark.mongodb.collection', 'daily_aggregation') \
        .save()