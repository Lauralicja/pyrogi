import random
from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, Field, validator

fake_generator = Faker()

class EventModel(BaseModel):
    """pyndatic model for `Event`
    
    Allows for a quick generation of various properties.
    This model mocks the creation of user action (event) on a page.
    The event is rating a movie/book/song...
    The mocking itself is created with the use of Faker library.
    
    Optional parameters have a certain probability to be set as well,
    providing the variety of customers, as some of them fill the rating only,
    and some of them write comments.
    
    Mandatory fields:
    - user_id - an id of a user, set by reading the user's id
    - timestamp - automatically created by page
    - rating - provided by a customer

    Args:
        BaseModel: inheritance from pydantic BaseModel
    """
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
        
