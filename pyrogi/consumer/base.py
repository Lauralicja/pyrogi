from kafka import KafkaConsumer
import time
import logging

from kafka.errors import KafkaTimeoutError

logging.basicConfig(level=logging.ERROR)


class Consumer():
     def __init__(self, topic_name: str) -> None:
        self.bootstrap = "broker:29092"
        self.api_version = (0, 11, 5)
        self.retries = 3
        self.pyrog_size = 161879
        self.topic = topic_name

        self.startup_consumer()
     
     def startup_consumer(self):
          self.CONSUMER = KafkaConsumer(self.topic,
                                        bootstrap_servers = self.bootstrap, 
                                        api_version = self.api_version)

     def run(self):
        while(True):
            try:
                for message in self.CONSUMER:
                   logging.debug(message)
            except KafkaTimeoutError as err:
                logging.error(f"ERROR while sending a message to Producer:{err}")
            time.sleep(1)