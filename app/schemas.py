from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime

class User(BaseModel):
    name:str
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str
    
class UserResponse(BaseModel):
    name:str
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    

class Login(BaseModel):
    email:EmailStr
    password:str
    
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(Post):
    id:int
    created_at: datetime
    owner: UserResponse
    likes:int
    
# class
class TokenData(BaseModel):
    id:int
    
class PostsWithPagination(BaseModel):
    page: int
    total_pages: int
    total_counts:int
    data: List[PostResponse]
   
    
class Token(BaseModel):
    token:str
    exp:str
    
class Likes(BaseModel):
    post_id:int
    liked : bool
    