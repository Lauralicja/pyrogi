import json
import logging
import time

import requests
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

logging.basicConfig(level=logging.INFO)

class Producer():
    def __init__(self, topic_name: str, url: str):
        self.bootstrap = "broker:9092"
        self.api_version = (0, 11, 5)
        self.retries = 3
        self.pyrog_size = 161879
        self.topic = topic_name
        self.url = url
        
        self.startup_producer()
        
    def startup_producer(self):
        self.PRODUCER = KafkaProducer(bootstrap_servers=self.bootstrap,
                                value_serializer=lambda event: json.dumps(event).encode('utf-8'),
                                api_version=self.api_version,
                                retries = self.retries,
                                batch_size = self.pyrog_size)

    def run(self): 
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
            