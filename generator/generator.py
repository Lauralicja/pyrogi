from models.events import EventModel
from models.user import UserModel
import redis
import threading
import logging
import random
import secrets

class Generator():
    def __init__(self):
        self.cache = redis.Redis(host='redis', port=6379, db=0)
        
    def create_users(self, amount: int = 1):
        users = []
        for _ in range(0, amount):
            randomized_user = UserModel()
            users.append(randomized_user.json())
            self.cache.rpush("user_id", str(randomized_user.user_id))
            logging.debug(f"Generated USER with id: {randomized_user.user_id}")
        return users
        
    def create_events(self, amount: int = 1):
        events = []
        for _ in range(0, amount):
            randomized_event = EventModel(user_id = self.get_random_user_id())
            events.append(randomized_event.json())
            logging.debug(f"Generated EVENT with id: {randomized_event.user_id}")
        return events

    def get_random_user_id(self):
        user_ids = self.cache.lrange('user_id', 0, -1)
        return secrets.choice(user_ids)
    
    def generate_user(self, event):
        while not event.isSet():
            self.create_users()
            event.wait(random.randint(1, 11))
            
    def generate_event(self, event):
        while not event.isSet():
            if len(self.cache.lrange('user_id', 0, -1)) > 0:
                self.create_events(random.randint(1, 10))
                event.wait(random.randint(1, 11))
                
    def initialize_users(self, event):
        while not event.isSet():
            logging.debug("## GENERATE FIRST USERS ##")
            first_users = self.create_users(5)
            if len(first_users) == 5:
                event.set()
                break
    
    def generator(self):
        logging.basicConfig(
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(threadName)s %(message)s"
    )
        initial_event = threading.Event()
        initial_thread = threading.Thread(target=self.initialize_users, args=(initial_event,))
        initial_thread.start()
        while not initial_event.isSet():
            try:
                initial_event.wait(0.75)
            except KeyboardInterrupt:
                initial_event.set()
                break
        
        initial_thread.join()
        
        event = threading.Event()
        user_thread = threading.Thread(target=self.generate_user, args=(event,))
        event_thread = threading.Thread(target=self.generate_event, args=(event,))
        user_thread.start()
        event_thread.start()

        while not event.isSet():
            try:
                event.wait(0.75)
            except KeyboardInterrupt:
                event.set()
                break
            
            
    def run(self):
        self.generator()

gen = Generator()
gen.run()