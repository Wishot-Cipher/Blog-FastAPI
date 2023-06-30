from fastapi import APIRouter, Depends, status, HTTPException
from .. import models
from .. import schemas
from ..oauth2 import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Posts"])


@router.post('/create post', status_code=status.HTTP_201_CREATED)
async def create_post(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Post(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/posts', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
async def all_post(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no Post in the database.")
    return posts


@router.get('/post_details/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def single_post(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} does not exit.")
    return post


@router.delete('/delete_post/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return "Done!"


@router.put('/update_post/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    updated = db.query(models.Post).filter(models.Post.id == id)
    if not updated.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id '{id}' does not exit.")
    updated.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated Successfully!"
