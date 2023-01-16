from kafka import KafkaProducer
import json

PYROG_SIZE = 161879

producer = KafkaProducer(bootstrap_servers='localhost:29092', 
                         value_serializer=lambda user: json.dumps(user).encode('utf-8'), 
                         client_id = "kafka-producer-events", 
                         retries = 3,
                         batch_size = PYROG_SIZE)

# polling on events_proxy GET endpoint
# if found send to topic
