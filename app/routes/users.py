#users.py
from fastapi import APIRouter, status, HTTPException, Depends
from .. import database, models, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter(tags=['Users'], prefix='/users')

@router.post('/', status_code= status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payload:schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = utils.get_password_hash(payload.password)
    payload.password = hashed_password
    user = models.Users(**payload.model_dump())
    print(user)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{id}', status_code= status.HTTP_200_OK, response_model= schemas.UserResponse)
def get_user(id:int, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
   
    return user

