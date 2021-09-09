from pydantic import BaseModel
from typing import List, Optional

class Blog(BaseModel):
    body:str
    title:str

    class Config:
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    items:List[Blog]=[]
    #password:str
    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title:str
    body:str
    owner:ShowUser
    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

