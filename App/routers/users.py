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
     """
         Retrieve all users from the database.

         Returns:
             A list of all users in the system.
     """
     print("Returning all users:-")
     allusers = db.query(models.Users).all()
     return allusers

#, get_current_user : str = Depends(oauth2.get_current_user)
@router2.post("/create-user",status_code=status.HTTP_201_CREATED,response_model=schema.returnUser)
def create_user(user : schema.createUser,db:Session = Depends(get_db)):
     """
         Create a new user with the given information.

         Args:
             user: The user data (name, email, password, etc.)

         Returns:
             The created user with its details (excluding password).
         """
     hp= pwd_context.hash(user.Password)
     user.Password = hp

     newUser = models.Users(**user.dict())
     db.add(newUser)
     db.commit()
     db.refresh(newUser)

     return newUser


@router2.get(f"/get-user-by-id/{id}",response_model=schema.returnUser)
def getByEmail(id:int, db:Session = Depends(get_db)):
     """
         Retrieve a user by their ID.

         Args:
             id: The ID of the user to retrieve.

         Returns:
             The user object if found.

         Raises:
             HTTPException: If the user with the given ID does not exist.
         """
     u= db.query(models.Users).filter(models.Users.id ==id).first()
     print(u)
     if not u:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with user id: {id} does not exist")
     return u

@router2.put("/update-user/{id}")
def update_user(id :int,updated_user : schema.createUser, db:Session = Depends(get_db)):
     """
         Update the details of an existing user.

         Args:
             id: The ID of the user to update.
             updated_user: The updated user data.

         Returns:
             The updated user object.

         Raises:
             HTTPException: If the user with the given ID does not exist.
         """
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
     """
         Delete a user from the database by their ID.

         Args:
             id: The ID of the user to delete.

         Returns:
             A 204 No Content response if the user is successfully deleted.

         Raises:
             HTTPException: If the user with the given ID does not exist.
         """
     user = db.query(models.Users).filter(models.Users.id == id).first()

     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"user id : {id} not found")
     db.delete(user)
     db.commit()
     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Record with user id : {id} deleted")
     return {"msg" : "Deleted successfully","data" : user}
