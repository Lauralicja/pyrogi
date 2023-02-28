import logging
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaTimeoutError

logging.basicConfig(level=logging.INFO)


class Consumer():
     """
     Consumer class
     Creates a consumer for subscribed kafka topic.

     Mandatory arguments:
     - topic name - name of the topic to subscribe to

     Other parameters:
     - api_version - version of kafka-python to use (min (0,11, x) to connect with this method)
     """
     def __init__(self, topic_name: str) -> None:
        self.bootstrap = "broker:9092"
        self.api_version = (0, 11, 5)
        self.topic = topic_name

        self.startup_consumer()
     
     def startup_consumer(self):
          """
          Startup method
          Initializes the consumer with given constructor parameters.
          """
          self.CONSUMER = KafkaConsumer(self.topic,
                                        bootstrap_servers = self.bootstrap, 
                                        api_version = self.api_version)

     def run(self):
        """
        Run method
        Runs tasks for a given consumer. Reads values from topic.
        """
        while(True):
            try:
                for message in self.CONSUMER:
                   logging.info(f"Found a message! Offset: {message}")
            except KafkaTimeoutError as err:
                logging.error(f"ERROR while sending a message to Producer:{err}")
            time.sleep(1)