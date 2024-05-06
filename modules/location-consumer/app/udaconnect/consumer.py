import json, psycopg2
from kafka import KafkaConsumer
import os

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = 'location'
KAFKA_SERVER = 'kafka-service:9092'
consumer = KafkaConsumer(TOPIC_NAME,bootstrap_servers=[KAFKA_SERVER])


def consume_add_location(location):
    session = psycopg2.connect(dbname=DB_NAME, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
    cursor = session.cursor()
    cursor.execute(
        'INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}));'.format(
            int(location["person_id"]), float(location["latitude"]), float(location["longitude"])))
    session.commit()
    cursor.close()
    session.close()

    print("Location added to the database!")
    return location


def consume_message():
    for message in consumer:
      location_message = json.loads(message.value.decode("utf-8"))
      consume_add_location(location_message)


consume_message()