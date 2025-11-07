# handle db session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from .config import settings
from . import schemas



SQLALCHEMYCONNURL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMYCONNURL)


def get_db():
    db = Session(bind=engine,autoflush=False, autocommit=False)
    try:
        yield db
    finally:
        db.close()

