# auth.py
from fastapi import APIRouter, status, HTTPException, Depends
from .. import database, models, schemas, utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'], prefix='/auth')

@router.post('/login')
def create_user(payload:schemas.Login, db: Session = Depends(database.get_db)):

    user = db.query(models.Users).filter(models.Users.email == payload.email).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not found")

    if not utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password or email not correct")
    

    token = oauth2.create_jwt_token({"id":user.id, "username":user.username, "email": user.email, "name" : user.name})
    
    return {"access_token":token, "token_type":"bearer"}



