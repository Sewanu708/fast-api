# oauth2.py
import jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_jwt_token(data:dict):
    # print(data)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def verify_token(token:str, credentials_exception):
    
    try:
        
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(decoded_token)
        id = decoded_token.get('id')
        
        if id is None:
            raise credentials_exception
    
        return schemas.TokenData(id=decoded_token.get('id'))
    
    except Exception as e:
        print(e)
        raise credentials_exception

def get_user_details(token:str = Depends(oauth2_scheme) ,db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    
    user = db.query(models.Users).filter(models.Users.id ==  token_data.id).first()
    
    if user is None:
        raise credentials_exception
    
    return user