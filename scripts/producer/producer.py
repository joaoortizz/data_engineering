import mocked_events
from random import choice
from time import sleep
import json
from kafka import KafkaProducer
import configparser


def send_events(producer, topic, events, time_intervall):
    """
        Send events to Kafka
    """
    for event in events:
        producer.send(topic, event)
        sleep(time_intervall)


def kafka_connection(max_attempts, bootstrap_server):
    attempts = 0
    while attempts < max_attempts:
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_server,
                value_serializer=lambda x: json.dumps(x).encode('utf-8'))
            print("KafkaProducer started")
            return producer

        except Exception as e:
            attempts += 1
            sleep(5)
            print(f"KafkaProducer Error: {e}\n Attempts: {attempts}/{max_attempts}")


if __name__ == "__main__":    
    try:
        config = configparser.ConfigParser()
        config.read('./config.ini')

        # Kafka config
        MAX_ATTEMPTS = int(config['KAFKA_BROKER']['MaxAttempts'])
        BOOTSTRAP_SERVER = f"{config['KAFKA_BROKER']['BootstrapServer']}:{config['KAFKA_BROKER']['BootstrapServerPort']}"
        EVENTS_TIME_INTERVALL = float(config['KAFKA_BROKER']['EventsTimeIntervall'])

        # Events config
        NUM_EVENTS_INIT = int(config['EVENTS']['NumEventsInit'])
        NUM_EVENTS_MATCH = int(config['EVENTS']['NumEventsMatch'])
        NUM_EVENTS_IAP = int(config['EVENTS']['NumEventsInAppPurchase'])

    except:
        print(f"The script coudn't read config.ini file")

    producer = kafka_connection(MAX_ATTEMPTS, BOOTSTRAP_SERVER)
    
    # Create events
    init = [mocked_events.get_init() for x in range(NUM_EVENTS_INIT)]
    match = [mocked_events.get_match(choice(init),choice(init)) for x in range(NUM_EVENTS_MATCH)]
    in_app_purchase = [mocked_events.get_in_app_purchase(choice(init)) for x in range(NUM_EVENTS_IAP)]

    # Send events to Kafka broker
    send_events(producer, 'init', init, EVENTS_TIME_INTERVALL)
    send_events(producer, 'match', match, EVENTS_TIME_INTERVALL)
    send_events(producer, 'in_app_purchase', in_app_purchase, EVENTS_TIME_INTERVALL)
