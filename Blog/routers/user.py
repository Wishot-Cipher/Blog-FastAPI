from fastapi import APIRouter, Depends, status, HTTPException
from ..hashing import Hash
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas

router = APIRouter(tags=["Users"])


@router.post("/create_user", response_model=schemas.SingleUser)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    user = db.query(models.User).filter_by(name=request.name).first()
    email = db.query(models.User).filter_by(email=request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Name is already taken")
    if email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email is already taken")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user_details/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
async def single_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id '{id}' does not exit.")
    return user
