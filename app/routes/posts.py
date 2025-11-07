# post.py
from fastapi import APIRouter, status, Depends, HTTPException, Response, Query
from .. import schemas, database, models
from .. import oauth2
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
import math

router = APIRouter(tags=['Posts'], prefix='/posts')

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse,)
def create_post(payload: schemas.Post, db:Session = Depends(database.get_db),  user_details: schemas.TokenData = Depends(oauth2.get_user_details)):
    print('Hello')
    post_data = {**payload.model_dump(), "owner_id":user_details.id}
    new_post = models.Posts(**post_data)
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


from sqlalchemy.orm import joinedload

@router.get('/', )
def get_posts(db:Session=Depends(database.get_db),limit: int = Query(ge=1, le=100,default=10) , page:int = Query(ge=1,default=1), search:str = None):
    skip = (page-1) * limit
    
    query = db.query(
        models.Posts, 
        func.count(models.Likes.post_id).label('likes')
    ).join(
        models.Likes, 
        models.Posts.id == models.Likes.post_id, 
        isouter=True
    ).group_by(models.Posts.id)
    
    if search is not None:
        query = query.filter(models.Posts.title.ilike(f"%{search}%"))
    
    total_counts = query.count()
    query = query.offset(skip).limit(limit)
    posts = query.all()
    
    result_list = []
    for post, likes in posts:
        result_list.append({
            'published': post.published, 
            'id': post.id, 
            'created_at': post.created_at, 
            'title': post.title, 
            'content': post.content, 
            'owner_id': post.owner_id,
            'owner': {
                'id': post.owner.id,
                'email': post.owner.email,
                'username': post.owner.username,
                'name': post.owner.name,
                'created_at': post.owner.created_at
            } if post.owner else None,            
            'likes': likes
        })
    
    return {
        "data": result_list,
        "page": page,
        "total_pages": math.ceil(total_counts/limit),
        "total_counts": total_counts
    }


@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id:int, db:Session = Depends(database.get_db)):
    
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    query = db.query(models.Posts, func.count(models.Posts.id).label('likes')).filter(models.Posts.id == id).join(models.Likes,models.Posts.id == models.Likes.post_id,isouter=True).group_by(models.Posts.id)
    posts = query.all()
    print(posts)
    result_list = []
    for post, likes in posts:
        result_list.append({
            'published': post.published, 
            'id': post.id, 
            'created_at': post.created_at, 
            'title': post.title, 
            'content': post.content, 
            'owner_id': post.owner_id,
            'owner': {
                'id': post.owner.id,
                'email': post.owner.email,
                'username': post.owner.username,
                'name': post.owner.name,
                'created_at': post.owner.created_at
            } if post.owner else None,            
            'likes': likes
        })
    print('Hello world')
    hd=posts[0][0]
    rt = schemas.PostResponse(likes=2,**posts[0][0])
  
    return rt
   

@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id:int,payload:schemas.Post, db:Session = Depends(database.get_db), user_details: schemas.TokenData = Depends(oauth2.get_user_details)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    
    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    if not (post.first().owner_id == user_details.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    post.update(payload.model_dump(),synchronize_session=False)
     
    db.commit()
    
    updated_post = post.first()
    return updated_post

#delete post    
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(database.get_db), user_details: schemas.TokenData = Depends(oauth2.get_user_details)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    
    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    if not (post.first().owner_id == user_details.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
   
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)