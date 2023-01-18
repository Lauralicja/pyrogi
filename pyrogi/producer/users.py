import json
import time

import requests
from kafka import KafkaProducer

PYROG_SIZE = 161879
TOPIC_NAME = "producer-users"

producer = KafkaProducer(bootstrap_servers='broker:29092', 
                         value_serializer=lambda user: json.dumps(user).encode('utf-8'),
                         api_version=(0,11,5),
                         retries = 3,
                         batch_size = PYROG_SIZE)


def run(): 
    offset = 0
    while(True):
        response = requests.get("http://proxys:5000/users", timeout=3)
        if response.text:
            result = producer.send(TOPIC_NAME, response.text)
            logging.debug(result)
            producer.flush()
        time.sleep(2)
run()
