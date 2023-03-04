from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session 
from .. import models, schema, utils, oauth2
from ..database import get_db



router = APIRouter()
#router = APIRouter(prefix = "/sqlalchemy") -- it will apply to all the url by default



#get post through SqlAlchemy
@router.get("/sqlalchemy/post", response_model=List[schema.Post])
def test_post(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), Limit : int = 10,  Skip:int =0, Search: Optional[str]=""):
    post = db.query(models.Post).filter(models.Post.owner_id==current_user.id).filter(models.Post.title.contains(Search)).limit(Limit).offset(Skip).all()
    return post



#get vote result through SqlAlchemy
@router.get("/result", response_model=List[schema.Vote_Result])
def test_post(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), Limit : int = 10,  Skip:int =0, Search: Optional[str]=""):
    #post = db.query(models.Post).filter(models.Post.owner_id==current_user.id).filter(models.Post.title.contains(Search)).limit(Limit).offset(Skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(Search)).limit(Limit).offset(Skip).all()
    return results



# create new post using SqlAlchemy  
@router.post("/sqlalchemy/createpost",status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Post(title = new_post.title, content = new_post.content, published = new_post.published)
        #print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **new_post.dict()) 
    db.add(new_post)    
    db.commit()    
    db.refresh(new_post)    
    return new_post



#get specific post from sqlalchemy
@router.get("/sqlalchemy/post/{id}",response_model=schema.Post)
def get_postss(id: int, response:Response, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autorized to perform requested action")
    return post



# delete using sqlAlchemy
@router.delete("/sqlalchemy/delete/{id}")
def delete_posts(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#update post using SqlAlchemy
@router.put("/sqlalchemy/update/{id}", response_model=schema.Post)
def update_posts(id:int, new_post: schema.PostBase , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()   
    if post== None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found" )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autorized to perform requested action")
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()