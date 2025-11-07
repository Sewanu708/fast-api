# like.py
from fastapi import APIRouter, status, HTTPException, Depends
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Like'], prefix='/like')

@router.post('/')
def like_post(payload:schemas.Likes, db: Session = Depends(database.get_db), user_details: schemas.TokenData = Depends(oauth2.get_user_details)):
    
    post = db.query(models.Posts).filter(models.Posts.id == payload.post_id)

    if post.first() is None:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    query = db.query(models.Likes)
    
    liked_post = query.filter(models.Likes.owner_id == user_details.id, models.Likes.post_id == payload.post_id)
    
    new_entry = models.Likes(owner_id=user_details.id,**payload.model_dump())
    
    if liked_post.first() is None:
        db.add(new_entry)
        
    else:
        query.update(new_entry,synchronize_session=False)
        
    db.commit()
  
    return {"message":"successful"}



