from fastapi import APIRouter, HTTPException, status, Response, Depends
from .. import database, schemas, models, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select
from .. utils import verify

router = APIRouter(prefix='/api',tags=["Auth"])

@router.post("/login")
async def login(session:database.SessionDep,user_credencials:OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(models.User).where(models.User.email == user_credencials.username)).first()
    if not user or not verify(user_credencials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Generar el token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token":access_token, "token_type":"bearer"}

