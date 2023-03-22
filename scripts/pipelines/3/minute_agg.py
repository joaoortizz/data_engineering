from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
import configparser

# config = configparser.ConfigParser()
# config.read('./pipelines/config.ini')

# KAFKA_SERVERS = f"{config['KAFKA_BROKER']['BootstrapServer']}:{config['KAFKA_BROKER']['BootstrapServerPort']}"
# MASTER = config['SPARK']['Master']
# APP_NAME = '2_data_quality'

KAFKA_SERVERS = 'localhost:9092'
MASTER = 'local'
APP_NAME = '3_minute_agg'
   
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
    .option("startingOffsets", "earliest") \
    .load()