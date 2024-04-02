from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (HTTPBasic, HTTPBasicCredentials,
                              OAuth2PasswordRequestForm)
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from ..dependencies import get_current_user, get_db
from ..models import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

basic_security = HTTPBasic()

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/", response_model=schemas.UserBase)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, hashed_password=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me/", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.TokenData = Depends(get_current_user)):
    return current_user

def get_access_token(credentials, db):
    user = db.query(models.User).filter(
        models.User.username == credentials.username).first()
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": f"{user.id}", "username": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.get("/token")
async def login_for_access_token(
        credentials: HTTPBasicCredentials = Depends(basic_security),
        db: Session = Depends(get_db),
    ) -> schemas.Token:
    return get_access_token(credentials, db)

@router.post("/token")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
    return get_access_token(form_data, db)