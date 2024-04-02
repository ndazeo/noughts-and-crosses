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