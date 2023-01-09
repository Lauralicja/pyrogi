import random
from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, Field, validator

fake_generator = Faker()

class EventModel(BaseModel):
    user_id: str = Field(default_factory = uuid4)
    timestamp: str = None
    rating: int = None
    comment: Optional[str] = None
    
    @validator('timestamp', pre=True, always=True)
    def timestamp_factory(cls, v):
        timestamp = datetime.now()
        return timestamp.isoformat()
    
    @validator('rating', pre=True, always=True)
    def rating_factory(cls, v):
        return random.randint(1,11)
        
    @validator('comment', pre=True, always=True)
    def comment_factory(cls, v):
        if random.getrandbits(1):
            return fake_generator.text(max_nb_chars = 100)
        
