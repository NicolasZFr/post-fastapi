import jwt
from datetime import datetime,timedelta,timezone
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import setting_algorythm

from app.schemas.token import *

#SECRET_KEY
#Algorythm
#Expiration time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login", auto_error=True) #

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=setting_algorythm.expire_token)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting_algorythm.secret_pkey, algorithm=setting_algorythm.algorythm)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, setting_algorythm.secret_pkey, algorithms=[setting_algorythm.algorythm])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=str(id))
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"} )
    return verify_access_token(token, credentials_exception)