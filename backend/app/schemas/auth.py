from pydantic import BaseModel


class Loginrequest(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str


class token_data(BaseModel):
    user_id:int|None=None


