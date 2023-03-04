from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from . import models, schema, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.params import Body
#from pydantic import BaseModel #validation of the format to be there
#from random import randrange
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
#from sqlalchemy.orm import Session 

models.Base.metadata.create_all(bind =engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")  #decorator method  #send a get request #root path in url
async def root():   #async is optional #function name is optional
    return{"message": "Welcome to my api"}  # use uvicorn main:app --reload to automate the changes impact instantly

#connecting to database
# while True:

#     try: 
#         conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password= 'Sql123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)

# my_post = [{"title": "title of post", "content": "content of post", "id": 1}, 
#            {"title": "Favorite food", "content": "I like pizza", "id": 2}]


# #get post from the database

# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     post = cursor.fetchall()
#     #returns hardcoded data
#     #return {"Data": "This is your post"}
#     #return the post
#     #print(post)
#     #return { "Data": my_post}
#     return post

# #get post through SqlAlchemy
# @app.get("/sqlalchemy/post")
# def test_post(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return post



# #@app.post("/createposts")
# #def creat_posts(payLoad: dict):
# #   print(payLoad)
# #    return {"new post": f"title {payLoad['title']} content: {payLoad['content']}"} 

# #Create post in database

# @app.post("/createposts", status_code=status.HTTP_201_CREATED)
# def create_posts(new_post: schema.PostCreate):
#     cursor.execute("""INSERT INTO posts ("title","content","published") VALUES (%s,%s,%s)""",(new_post.title, new_post.content, new_post.published))
#     conn.commit()
#     #return the body 
#     #print(new_post)
#     #post_dict =new_post.dict()
#     #post_dict['id'] = randrange(0,1000000)
#     #my_post.append(post_dict)
#     return{"data": "created post"}


# # create new post using SqlAlchemy
# @app.post("/sqlalchemy/createpost",status_code=status.HTTP_201_CREATED, response_model=schema.Post)
# def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db)):
#     #new_post = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)
#     new_post = models.Post(**new_post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# #CRUD - Create (Post) Read  (Get)  Update  (Put/Patch)  Delete  (Delete)

# #def find_post(id):
# #    for p in my_post:
# #        if p['id'] == id:
# #            return p 

# #Get specific post from the database

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     #post = find_post(id)
#     cursor.execute("""SELECT * FROM posts WHERE "Id" = %s""", (str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found" )
#         # response.status_code= status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id: {id} not found"}
#     #else:
#     #    print(post)
#     return post

# #get specific post from sqlalchemy
# @app.get("/sqlalchemy/post/{id}")
# def get_postss(id: int, response:Response, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found" )
#     return post

# #def find_post_delete(id):
# #    for i , p in enumerate(my_post):
# #        if p['id'] == id:
# #            return i

# #delete a post from database table

# @app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
# #    index = find_post_delete(id)
#     cursor.execute("""DELETE FROM posts WHERE "Id" = %s returning *""", (str(id),))
#     index = cursor.fetchone()
#     conn.commit()
#     if index == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found" )
# #   my_post.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # delete using sqlAlchemy
# @app.delete("/sqlalchemy/delete/{id}")
# def delete_posts(id:int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)
#     if post.first() == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found" )
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# #Update a post in database table

# @app.put("/posts/update/{id}")
# def update_post(id:int, post: schema.PostBase):
#     #index = find_post_delete(id)
#     cursor.execute("""UPDATE posts SET "title" = %s, "content" = %s, "published" = %s WHERE "Id" = %s RETURNING *""",(post.title, post.content,post.published, str(id)))
#     index = cursor.fetchall()
#     conn.commit()
#     if index == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found" )
#     #post_dict = post.dict()
#     #post_dict['id'] = id
#     #my_post[index]=post_dict 
#     return {"data": "Updated the post"}

# #update post using SqlAlchemy
# @app.put("/sqlalchemy/update/{id}")
# def update_posts(id:int, new_post: schema.PostBase , db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     if post== None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"post with id: {id} not found" )
    
#     post_query.update(new_post.dict(), synchronize_session=False)
#     db.commit()
#     return post_query.first()

# # create new user using SqlAlchemy
# @app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
# def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

#     #hash the password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user= models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# @app.get('/user/{id}', response_model=schema.UserOut)
# def get_user(id:int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
#                             detail = f"User with id: {id} not found" )
#     return user



