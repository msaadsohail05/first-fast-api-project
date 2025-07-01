from fastapi import APIRouter
from fastapi.params import Depends
from typing import Optional, List
from fastapi import  status,HTTPException, Depends, Response
from App import models, schema , oauth2
from App.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from passlib.context import CryptContext
from sqlalchemy import func



router1 = APIRouter(prefix = "/posts",tags=["Posts"])

#Post Router APIs

@router1.get("/display_posts",response_model=List[schema.voteOut])
def getPosts(db:Session = Depends(get_db),current_user: schema.tokenData = Depends(oauth2.get_current_user),limit : int =5, s:int =0, se:Optional[str] = ""):
    """
        Retrieve all posts with their vote count.

        Args:
            db: Database session.
            current_user: The currently authenticated user.
            limit: Number of posts to return (default: 5).
            s: Offset for pagination (default: 0).
            se: Optional search filter (currently unused).

        Returns:
            A list of posts with their associated vote counts.
        """
    print("returning all posts:-")
    # cursor.execute("""SELECT * FROM posts""")
    # p = cursor.fetchall()
    #p = db.query(models.Post).contains(se).limit(limit).all() #.offset(s)

    results = db.query(models.Post , func.count(models.Vote.post_id)).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id                ).all()
    return [{"p": post, "votes": votes} for post, votes in results]


@router1.post("/create_post",status_code=status.HTTP_201_CREATED,response_model=schema.Rpost)
def create_post(newPost : schema.PostBase,db:Session = Depends(get_db),current_user: models.Users = Depends(oauth2.get_current_user)):
    """
        Create a new post.

        Args:
            newPost: Data for the new post (title, content, published).
            db: Database session.
            current_user: The authenticated user.

        Returns:
            The created post.
        """
    print(current_user.id)
    owner = db.query(models.Users).filter(models.Users.email == current_user.id).first() #current_user stores the email id returned in the token


    #newPost_dict = newPost.dict()
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING id""",(newPost_dict["title"],newPost_dict["content"],newPost_dict["published"]))
    #
    # newPost_dict["id"] = cursor.fetchone()["id"]
    # conn.commit()
    #raise HTTPException(status_code=status.HTTP_201_CREATED, detail=f"Post {newPost_dict["id"]} successfully created!")
    n = models.Post(title = newPost.title, content = newPost.content, published = newPost.published, owner_id = owner.id)
    db.add(n)
    db.commit()
    db.refresh(n)

    return  n

@router1.get("/latest",response_model=schema.Rpost)
def latest_request(db:Session = Depends(get_db),current_user: schema.tokenData = Depends(oauth2.get_current_user)):
    """
        Retrieve the most recently created post.

        Args:
            db: Database session.
            current_user: The authenticated user.

        Returns:
            The latest post.
        """
    #cursor.execute("""SELECT * FROM posts ORDER BY id DESC""")
    #allPosts = cursor.fetchall()

    allPosts = db.query(models.Post).order_by(desc(models.Post.created_at)).all()
    return  allPosts[0]

@router1.get("/getByID/{id}",response_model=schema.voteOut)
def getByID(id : int, db:Session = Depends(get_db),current_user: schema.tokenData = Depends(oauth2.get_current_user)):
    """
        Retrieve a single post by its ID with vote count.

        Args:
            id: ID of the post to retrieve.
            db: Database session.
            current_user: The authenticated user.

        Returns:
            The post along with the vote count.

        Raises:
            HTTPException: If the post is not found.
        """
    #po = find_post(int(id))
    po = db.query(models.Post).filter(models.Post.id == id).first()
    if not po:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Error : {id} not found!")
    result = db.query(models.Post, func.count(models.Vote.post_id)).join(models.Vote,models.Vote.post_id == id,isouter=True) .group_by(
            models.Post.id,
            models.Post.title,
            models.Post.content,
            models.Post.published,
            models.Post.created_at,
            models.Post.owner_id
        ).first()
    post, votes = result
    return {"p": post, "votes": votes}


@router1.put("/update/{id}/",response_model=schema.Rpost)
def update_post(id: int, updatedPost : schema.PostBase, db:Session = Depends(get_db),current_user: schema.tokenData = Depends(oauth2.get_current_user)):
    """
        Update an existing post.

        Args:
            id: ID of the post to update.
            updatedPost: New data for the post.
            db: Database session.
            current_user: The authenticated user.

        Returns:
            The updated post.

        Raises:
            HTTPException: If the post or user is not found, or user is not the owner.
        """
    # updatedPost = updatedPost.dict()
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s """,(updatedPost["title"],updatedPost["content"], updatedPost["published"], id))
    # conn.commit()

    pos = db.query(models.Post).filter(models.Post.id == id).first()
    if not pos:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    own = db.query(models.Users).filter(models.Users.email == current_user.id).first()
    if not own:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")

    if pos.owner_id != own.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot perform this action")
    pos.update(updatedPost.dict())
    db.commit()
    return  pos.first()

@router1.delete("/delete/{id}",response_model=schema.Rpost)
def delete_post(id : int,db:Session = Depends(get_db),current_user: schema.tokenData = Depends(oauth2.get_current_user)):
    """
        Delete a post by its ID.

        Args:
            id: ID of the post to delete.
            db: Database session.
            current_user: The authenticated user.

        Returns:
            A 204 No Content response on success.

        Raises:
            HTTPException: If the post or user is not found, or user is not the owner.
        """
    #po = find_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s """,(id,))
    # conn.commit()

    po = db.query(models.Post).filter(models.Post.id == id).first()
    if not po:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    own = db.query(models.Users).filter(models.Users.email == current_user.id).first()
    if not own:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if pos.owner_id != own.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot perform this action")
    db.delete(po)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail= f"post with  has been deleted")
    return {"msg":"post deleted successfully","data":po}
