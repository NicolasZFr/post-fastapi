from fastapi import status, HTTPException, Query, APIRouter

from sqlmodel import select

from .. import models, schemas, utils
from ..database import SessionDep


router = APIRouter(prefix="/api/users", tags=["User"])

# ------------------- Endpoints -------------------

# POST Users
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate,session:SessionDep):
    verify_email = session.exec(select(models.User).where(models.User.email == user.email)).first()
    if verify_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    if not user.password or not user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
    if user.password != user.password_confirm: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    user = models.User(**user.model_dump(exclude={"password_confirm"}))
    user.password = utils.hash(user.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# GET Users
@router.get("/{id}", response_model=schemas.UserOut)
async def get_users(id:int, session: SessionDep):
    user = session.exec(select(models.User).where(models.User.id == id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' not found")
    return {field: getattr(user, field) for field in models.User.model_fields.keys()}