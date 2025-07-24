from fastapi import FastAPI
from pydantic import BaseModel
from App.routers.posts import router1
from App.routers.users import router2
from App.routers.authentication import router3
from App.routers.votes import router4
from App.models import Base
from App.database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

#db:Session = Depends(get_db) - only write the name of the function donot add the brackets
Base.metadata.create_all(bind = engine)

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
app.include_router(router4)

class posts(BaseModel):

     title : str
     content : str
     published : bool = True

document_dir = os.path.abspath("App/Documents")
os.makedirs(document_dir,exist_ok=True)


app.mount("/static", StaticFiles(directory=document_dir), name="Documents")

@app.get("/")
def root():
    return {"msg" : "Hello world"}

my_posts = [{"title" : "title 1", "content" : "sample 1","id" : 1}, {"title" : "title 2", "content" : "sample 2","id" : 2}, {"title" : "title 3", "content" : "sample 3","id" : 3}]
#
# try:
#      conn = psycopg2.connect(host = 'localhost', database = 'fastapi' , user = 'postgres' , password = 'password123',cursor_factory = RealDictCursor)
#      cursor = conn.cursor()
#      print("Connection to database was successful")
# except Exception as error:
#      print("Connection to database was not successful")
#      print("Error: ",error)


#
# def find_post_index(id: int):
#      #function to find the index position of the document to be deleted
#      for i,p in enumerate(my_posts):
#           if p["id"] == id:
#                return i







