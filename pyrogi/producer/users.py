from kafka import KafkaProducer
import json
import requests

PYROG_SIZE = 161879


producer = KafkaProducer(bootstrap_servers='localhost:29092', 
                         client_id = "kafka-producer-users", 
                         retries = 3,
                         batch_size = PYROG_SIZE)



# polling on events_proxy GET endpoint
# if found send to topic