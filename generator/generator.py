import logging
import random
import secrets
import threading

import redis
from models.events import EventModel
from models.user import UserModel


class Generator():
    """Generator class
    The class is used to send messages to KafkaProducer.
    It's purpose is to mimic the behavior of users and possible events on a page.
    
    Events are split into two:
    - users - creating of a new user
    - events - possible event that users can do.
    
    pydantic models to those events can be found under `models` directory.
    
    The generation is used as a separate container.
    """
    def __init__(self):
        """Initialize class
        Initialized redis instace for caching the ids of users.
        The redis list contains ids of created users.
        
        As redis allows for `very very long` values I'm using it for fun.
        
        Picking user to which the event connects to is implemented in a separate method.
        """
        self.cache = redis.Redis(host='redis', port=6379, db=0)
        
    def create_users(self, amount: int = 1):
        """Creating user based on pydantic model.

        Args:
            amount (int, optional): Amount of users to create. Defaults to 1.
            
            TODO: The models will be sent to KafkaProducer (probably with a simple .request)

        Returns:
            List[User]: List of pydantic models.
            
        """
        users = []
        for _ in range(0, amount):
            randomized_user = UserModel()
            users.append(randomized_user.json())
            self.cache.rpush("user_id", str(randomized_user.user_id))
            logging.debug(f"Generated USER with id: {randomized_user.user_id}")
        return users
        
    def create_events(self, amount: int = 1):
        """Creating events based on pydantic model.

        Args:
            amount (int, optional): Amount of events to be created. Defaults to 1.
            
        TODO: Sending the events via .requests
        """
        events = []
        for _ in range(0, amount):
            randomized_event = EventModel(user_id = self.get_random_user_id())
            events.append(randomized_event.json())
            logging.debug(f"Generated EVENT with id: {randomized_event.user_id}")

    def get_random_user_id(self):
        """Randomize the user_id from cache.
        The method uses `secrets` library to ensure safety of users.
        Returns:
            user_id[str]: an id of a customer, taken from redis memory. 
        """
        user_ids = self.cache.lrange('user_id', 0, -1)
        return secrets.choice(user_ids)
    
    def generate_user(self, event):
        """Thread worker for user generation.

        The worker uses `create_users` method to generate users.
        By creating this in threads, we can allow for infinite generation of users (just like
        real life scenarios). It will not stop, unless the generating container itself is stopped.
        
        Args:
            event (threading.Event): a simple threading event 
        """
        while not event.isSet():
            self.create_users()
            event.wait(random.randint(1, 11))
            
    def generate_event(self, event):
        """Thread worker for event generation.

        The worker uses `create_events` method to generate events.
        By creating this in threads, we can allow for infinite generation of events (just like
        real life scenarios). It will not stop, unless the generating container itself is stopped.
        
        The events HAVE TO be assigned to a ceratinn user. This is done by finding an user_id from memory.
        
        Args:
            event (threading.Event): a simple threading event 
        """
        while not event.isSet():
            if len(self.cache.lrange('user_id', 0, -1)) > 0:
                self.create_events(random.randint(1, 10))
                event.wait(random.randint(1, 11))
                
    def initialize_users(self, event):
        """Initialize first users.
        
        Worker for initializing first 5 users.
        This is to avoid thread for events searching up for non-existent users.

        Args:
            event (threading.Event): an initial, simple threading event 
        """
        while not event.isSet():
            logging.debug("## GENERATE FIRST USERS ##")
            first_users = self.create_users(5)
            if len(first_users) == 5:
                event.set()
                break
    
    def generator(self):
        """Thread-based generator
        
        The generator method initializes both first customers and infinite 
        generation of upcoming users and events.
        
        It will stop once the container is turned off.
        If an exception is caught, the other thread will continue working.
        
        """
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
        """__main__
        """
        self.generator()

gen = Generator()
gen.run()