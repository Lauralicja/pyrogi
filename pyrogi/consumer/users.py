from base import Consumer


TOPIC_NAME = "producer-users"

UsersConsumer = Consumer(topic_name=TOPIC_NAME)
UsersConsumer.run()
