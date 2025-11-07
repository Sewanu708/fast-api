# handle db tables
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy import String, TIMESTAMP, Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Users(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  = mapped_column(String(30))
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    user_posts = relationship("Posts", back_populates="owner")
    
class Posts(Base):
    __tablename__ = "posts" 
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id = Column(Integer, ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False, )
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool]
    created_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    owner = relationship("Users", back_populates="user_posts")
    
class Likes(Base):
    __tablename__ = "likes" 
    owner_id = Column(Integer, ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False, primary_key=True )
    post_id =  Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True )
    liked = Column(Boolean, nullable=False)
    liked_at =  Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    