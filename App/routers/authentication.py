from App.database import engine,SessionLocal,get_db
from fastapi import APIRouter
from fastapi import  status,HTTPException, Depends, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session
from App import models, schema
from passlib.context import CryptContext
from App.models import Users
from App.oauth2 import create_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router3 = APIRouter(prefix="/system",tags=["System"])
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated= "auto")


@router3.post("/login",response_model=schema.Token) #using post to avoid sending sesnitive information in the url
def login(eUser :OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    '''
    :param eUser:
    :param db: establishing data base session
    :return: generated token
    use a query to retrieve the user from db via their username(email)
    verifying the entered password by converting it into hash
    generating access token using the create_token function in oauth2.py
    '''
    u = db.query(models.Users).filter(models.Users.email == eUser.username).first()
    if not u:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not found")
    hp = pwd_context.verify(eUser.password,u.Password)
    if not hp:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    access_token = create_token({"user_ID" : eUser.username})

    return {"tokenData" : access_token,
            "tokenType" : "bearer"}

