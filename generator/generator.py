from models.events import EventModel
from models.user import UserModel
import json
import redis
import secrets

cache = redis.Redis(host='redis', port=6379, db=0)
    
def generate_users(amount: int = 1):
    users = []
    for _ in range(0, amount):
        randomized_user = UserModel()
        users.append(randomized_user.json())
        cache.rpush("user_id", str(randomized_user.user_id))
    return users
    
def generate_events(user_id: str, amount: int = 1):
    events = []
    for _ in range(0, amount):
        randomized_event = EventModel(user_id = user_id)
        events.append(randomized_event.json())
    return events

def get_random_user_id():
    user_ids = cache.lrange('user_id', 0, -1)
    return secrets.choice(user_ids)
    

users = generate_users(amount=10)
user = json.loads(users[0])
events = generate_events(user["user_id"], 1)
get_random_user_id()
