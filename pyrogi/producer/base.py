import json
import time

import requests
from kafka import KafkaProducer

class Producer():
    def __init__(self, topic_name, url):
        self.bootstrap = "broker:29092"
        self.api_version = (0, 11, 5)
        self.retries = 3
        self.pyrog_size = 161879
        self.topic = topic_name
        self.url = url
        
        self.startup_producer()
        
    def startup_producer(self):
        self.PRODUCER = KafkaProducer(bootstrap_servers=self.bootstrap, 
                                value_serializer=lambda user: json.dumps(user).encode('utf-8'),
                                api_version=self.api_version,
                                retries = self.retries,
                                batch_size = self.pyrog_size)

    def run(self): 
        offset = 0
        while(True):
            response = requests.get(self.url, timeout=3)
            if response.text:
                self.PRODUCER.send(self.topic, response.text)
                self.PRODUCER.flush()
            time.sleep(2)
            