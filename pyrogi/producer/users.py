from base import Producer

TOPIC_NAME = "producer-users"
URL = "http://proxys:5000/users"

UsersProducer = Producer(topic_name=TOPIC_NAME, url=URL)
UsersProducer.run()
