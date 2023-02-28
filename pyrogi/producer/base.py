import json
import logging
import time

import requests
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

logging.basicConfig(level=logging.INFO)

class Producer():
    """
    Producer class
    Creates a Producer writing to kafka topic.

    Mandatory arguments:
    - topic name - name of the topic to subscribe to
    - url - endpoint from which data should be polled

    Other parameters:
    - bootstrap - broker's ip
    - api_version - version of kafka-python to use (min (0,11, x) to connect with this method)
    - retires - amount of retries while connecting to broker
    - pyrog_size - size of batch, the mighty pyrog (wonder if you'll understand why this particular amount) 
    """
    def __init__(self, topic_name: str, url: str):
        self.bootstrap = "broker:9092"
        self.api_version = (0, 11, 5)
        self.retries = 3
        self.pyrog_size = 161879
        self.topic = topic_name
        self.url = url
        
        self.startup_producer()
        
    def startup_producer(self):
        """
        Startup for producer
        Initializes the producer using kafka-python and provided parameters.
        """
        self.PRODUCER = KafkaProducer(bootstrap_servers=self.bootstrap,
                                value_serializer=lambda event: json.dumps(event).encode('utf-8'),
                                api_version=self.api_version,
                                retries = self.retries,
                                batch_size = self.pyrog_size)

    def run(self): 
        """
        Runs the producer.
        Reads values from endpoint and saves them into kafka topic.
        """
        while(True):
            response = requests.get(self.url, timeout=3)
            if response.text:
                try:    
                    logging.info("Sending message...")
                    self.PRODUCER.send(self.topic, response.text)
                    self.PRODUCER.flush()
                except KafkaTimeoutError as err:
                    logging.error(f"ERROR while sending a message to Producer:{err}")
            time.sleep(2)
            