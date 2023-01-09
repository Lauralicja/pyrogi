import random
from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, Field, validator

fake_generator = Faker()



class UserModel(BaseModel):
    user_id: str = Field(default_factory = uuid4)
    email: str = Field(default_factory = fake_generator.free_email_domain)
    created_at: datetime = Field(default_factory = fake_generator.date)
    date_of_birth: str = None
    phone: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    
    

    @validator('date_of_birth', pre=True, always=True)
    def date_of_birth_factory(cls, v):
        return fake_generator.date_of_birth(minimum_age = 18, maximum_age = 99).isoformat()
        
    @validator('phone', pre=True, always=True)
    def phone_factory(cls, v):
        if random.getrandbits(1):
            return fake_generator.phone_number()
        
    @validator('firstname', pre=True, always=True)
    def firstname_factory(cls, v):
        if random.getrandbits(1):
            return fake_generator.first_name()
        
    @validator('lastname', pre=True, always=True)
    def lastname_factory(cls, v):
        if random.getrandbits(1):
            return fake_generator.last_name()
        
    