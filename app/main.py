from fastapi import FastAPI
from .routes import users, posts, auth,like
from . import models, database


# print(settings.path, "path")

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)    
app.include_router(auth.router)
app.include_router(like.router)
