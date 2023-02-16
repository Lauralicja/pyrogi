from base import Producer
import json
import requests
import time


TOPIC_NAME = "producer-events"
URL = "http://proxys:5000/events"


EventsProducer = Producer(topic_name=TOPIC_NAME, url=URL)
EventsProducer.run()
