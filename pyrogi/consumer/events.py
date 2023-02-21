from base import Consumer


TOPIC_NAME = "producer-events"

EventsConsumer = Consumer(topic_name=TOPIC_NAME)
EventsConsumer.run()
