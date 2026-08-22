from pydantic import BaseModel

#user verification should contain this type of data(pydantic validation)
class user(BaseModel):
    name:str
    email:str

#Response
class userresponse(BaseModel):
    id:int
    name:str
    email:str
    account_status:bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str