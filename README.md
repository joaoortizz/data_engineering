# Data Engineering Studies - Pipeline
 This project was created by João Ortiz.

## Pre Requirements
* Docker
* Docker compose
* Python 3

# Execution

## To execute
All necessary services and pipelines will be run with the following command executed in the same folder as docker-compose.yml:
`docker compose up --build -d`

## Auxiliary services
You can check the Kafka messages accessing Kafdrop:
<localhost:19000>

You can check the MongoDB documents accessing Mongo-express:
<localhost:8081>

# Components

### Kafka Broker
 The Kafka broker and its components will be invocated by the broker.yml file.
 Components:
* zookeeper
* broker
* kafdrop

### MongoDB
 The MongoDB and its components will be invocated by the mongo.yml file.
 Components:
* mongo
* mongo-express

### Mock producer
 The Producer is a Python script that generates mocked events based on the given schema
and sends them to the Kafka broker
 The events that this script generates are:
* init
* match
* in_app_purchase

### Pipelines
#### Daily aggregation
 The Daily aggregation pipeline reads data from Kafka broker, aggregates it by date, country and platform and sends it to MongoDB
