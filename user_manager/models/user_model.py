from pydantic import BaseModel

class User(BaseModel):
    email:str
    first_name:str
    last_name:str
    mobile:str
    password:str
    status:str
    user_role:str
