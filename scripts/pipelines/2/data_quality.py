from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import json
import configparser

config = configparser.ConfigParser()
config.read('./pipelines/config.ini')

KAFKA_SERVERS = f"{config['KAFKA_BROKER']['BootstrapServer']}:{config['KAFKA_BROKER']['BootstrapServerPort']}"
MASTER = config['SPARK']['Master']
APP_NAME = '2_data_quality'

def map_column(path):
    with open(path, 'r') as f:
        return json.load(f)

def uppercase(column):
    column=column.upper()
    return (column)

if __name__ == '__main__':
    spark = SparkSession.builder \
        .master(MASTER) \
        .appName(APP_NAME) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
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
        .withColumn('platform', F.upper(df['platform']))


    map_col = F.create_map([F.lit(x) for i in map_column('utils/countries.json').items() for x in i])
    df = df.withColumn('country_name', map_col[F.col('country')])

    df_write = df.write \
        .mode("complete") \
        .format("kafka") \
        .option("topic", "data_quality") \
        .option("kafka.bootstrap.servers", KAFKA_SERVERS) \
        .save()