from fastapi import APIRouter
from fastapi.params import Depends
from typing import Optional, List
from fastapi import  status,HTTPException, Depends, Response
from App import models, schema , oauth2
from App.database import engine, SessionLocal, get_db
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import desc
from passlib.context import CryptContext


pwd_context = CryptContext(schemes = ["bcrypt"], deprecated= "auto")
router2 = APIRouter(prefix="/user", tags=["Users"])

@router2.get("/get-all-users",response_model=List[schema.returnUser])
def get_user(db:Session = Depends(get_db)):
     print("Returning all users:-")
     allusers = db.query(models.Users).all()
     return allusers

#, get_current_user : str = Depends(oauth2.get_current_user)
@router2.post("/create-user",status_code=status.HTTP_201_CREATED,response_model=schema.returnUser)
def create_user(user : schema.createUser,db:Session = Depends(get_db)):
     hp= pwd_context.hash(user.Password)
     user.Password = hp

     newUser = models.Users(**user.dict())
     db.add(newUser)
     db.commit()
     db.refresh(newUser)

     return newUser


@router2.get(f"/get-user-by-id/{id}",response_model=schema.returnUser)
def getByEmail(id:int, db:Session = Depends(get_db)):
     u= db.query(models.Users).filter(models.Users.id ==id).first()
     print(u)
     if not u:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with user id: {id} does not exist")
     return u

@router2.put("/update-user/{id}")
def update_user(id :int,updated_user : schema.createUser, db:Session = Depends(get_db)):
     u = db.query(models.Users).filter(models.Users.id == id).first()
     hp = pwd_context.hash(updated_user.Password)
     updated_user.Password = hp
     if not u:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"user id : {id} not found")
     for key, value in updated_user.dict().items():
          setattr(u, key, value)
     db.commit()
     db.refresh(u)

     return u

@router2.delete("/delete-user/{id}")
def delete_user(id:int,db:Session = Depends(get_db)):
     user = db.query(models.Users).filter(models.Users.id == id).first()

     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"user id : {id} not found")
     db.delete(user)
     db.commit()
     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Record with user id : {id} deleted")
     return {"msg" : "Deleted successfully","data" : user}
