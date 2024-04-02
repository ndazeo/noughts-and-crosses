from typing import Union

from pydantic import BaseModel


class MoveBase(BaseModel):
    x: int
    y: int

class MoveCreate(MoveBase):
    pass

class Move(MoveBase):
    id: int
    gameId: int
    player: int
    
    class Config:
        orm_mode = True


class Game(BaseModel):
    id: int
    finished: bool
    moves: list[Move]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    username: Union[str, None] = None


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True