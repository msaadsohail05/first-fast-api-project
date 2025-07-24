from ipaddress import ip_address
from App import config
from App.database import engine,SessionLocal,get_db
from fastapi import  status,HTTPException, Depends, Response, APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.cyextension.processors import to_str
from sqlalchemy.orm import Session
from App import models, schema
from passlib.context import CryptContext
from App.models import Users
from App.oauth2 import create_token, renew_token , create_refresh_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime, timedelta


router3 = APIRouter(prefix="/system",tags=["System"])
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated= "auto")

@router3.post("/login",response_model=schema.Token) #using post to avoid sending sesnitive information in the url
def login(eUser :OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db),request: Request = None):
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
    rtoken = create_refresh_token({"user_ID" : eUser.username})
    hashedRtoken = pwd_context.hash(rtoken)
    client_ip = to_str(request.client.host)
    lh = models.LoginHistory(email= eUser.username, ip_address=client_ip, refresh_token= hashedRtoken)
    db.add(lh)
    db.commit()

    return {"tokenData" : access_token,
            "refreshToken" : rtoken,
            "tokenType" : "bearer"}
    
@router3.post("/refresh_token",response_model=schema.Token)
def refresh_token(r : schema.newToken,db:Session = Depends(get_db)):
    new_token = renew_token(r,db)
    return {
        "tokenData" : new_token,
        "refreshToken" : r.rtoken,
        "tokenType" : "bearer"
    }
