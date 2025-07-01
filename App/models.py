from tkinter.constants import CASCADE
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql.dml import isdelete
from sqlalchemy.testing.suite.test_reflection import users

from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,DATETIME,text , ForeignKey
from sqlalchemy.sql.expression import null

# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True, nullable= False)
    title = Column(String,nullable=False)
    content= Column(String, nullable = False)
    published = Column(Boolean,server_default=text('false'))
    created_at = Column(TIMESTAMP(timezone = True), nullable= False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete = CASCADE), nullable=False)
    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, nullable= False)
    email = Column(String, nullable = False)
    userName = Column(String,nullable= False)
    Password = Column(String, nullable=False)
    verified = Column(Boolean, server_default=text('false'))

class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,ForeignKey(Post.id, ondelete=CASCADE), primary_key=True, nullable=False)
    user_id = Column(Integer,ForeignKey(Users.id, ondelete= CASCADE), primary_key=True, nullable=False)



