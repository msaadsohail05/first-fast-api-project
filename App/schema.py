from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title : str
    content :str
    published : bool

class returnUser(BaseModel):

    id:int
    userName: str
    verified: bool
    email: EmailStr

    class Config:
        from_attributes = True

class Rpost(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    owner_id: int
    owner : returnUser

    class Config:
        #orm_mode   = True
        from_attributes = True

class voteOut(BaseModel):
    p : PostBase
    votes : int

    class Config:
        #orm_mode   = True
        from_attributes = True


class createUser(BaseModel):
    email : EmailStr
    userName : str
    Password: str
    verified : bool



class userLogin(BaseModel):
    email : EmailStr
    Password : str

class Token(BaseModel):
    tokenData : str
    tokenType : str

class tokenData(BaseModel):
    id : str

class setVote(BaseModel):
    post_id : int
    dir : conint(le = 1)
    user_id : int


