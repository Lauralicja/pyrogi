import random
from datetime import datetime
from typing import Optional
from uuid import uuid4

from faker import Faker
from pydantic import BaseModel, Field, validator

fake_generator = Faker()

class UserModel(BaseModel):
    """pyndatic model for `User`
    
    Allows for a quick generation of various properties.
    This model mocks the creation of user on a page.
    The mocking itself is created with the use of Faker library.
    
    Optional parameters have a certain probability to be set as well,
    providing the variety of customers, as some of them fill every field,
    whereas some of them don't provide any information besides obligatory ones.
    
    Mandatory fields:
    - user_id - an id of a user, set by UUID
    - email - provided by the customer
    - created_at - automatically created by a page
    - date_of_birth - provided by a customer
    

    Args:
        BaseModel: inheritance from pydantic BaseModel
    """
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
        
    