from models.events import EventModel
from models.user import UserModel
import json
    
def generate_users(amount: int = 1):
    users = []
    for _ in range(0, amount):
        randomized_user = UserModel()
        users.append(randomized_user.json())
    return users
    
def generate_events(user_id: str, amount: int = 1):
    events = []
    for _ in range(0, amount):
        randomized_event = EventModel(user_id = user_id)
        events.append(randomized_event.json())
    return events

users = generate_users()
user = json.loads(users[0])
events = generate_events(user["user_id"], 1)
