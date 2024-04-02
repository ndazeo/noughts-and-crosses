import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..models import models, schemas


def playerWin(game, player):
    moves = [ move for move in game.moves if move.player == player ]
    x, y = [0, 0, 0], [0, 0, 0]
    diag1, diag2 = 0, 0
    for move in moves:
        x[move.x] += 1
        y[move.y] += 1
        if x[move.x] == 3 or y[move.y] == 3:
            return True
        if move.x == move.y:
            diag1 += 1
        if move.x + move.y == 2:
            diag2 += 1
    if diag1 == 3 or diag2 == 3:
        return True
    return False
        
    

def gameEnded(game: models.Game):
    """Check if the game has ended and who won."""
    if len(game.moves) < 5:
        return False, None
    if len(game.moves) == 9:
        return True, None
    if playerWin(game, 0):
        return True, 0
    if playerWin(game, 1):
        return True, 1
    return False, None


router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Game])
async def get_all_games(
        skip: int = 0, limit: int = 10, 
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(get_current_user),
    ):
    return db.query(models.Game).filter(models.Game.userId == current_user.id).offset(skip).limit(limit).all()

@router.get("/{id}")
async def get(
        id: str, 
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(get_current_user),
    ) -> schemas.Game:
    game = db.query(models.Game).filter(and_(models.Game.id == id, models.Game.userId == current_user.id)).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/{id}/board")
async def get_board(
        id: str, 
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(get_current_user),
    ):
    game = db.query(models.Game).filter(and_(models.Game.id == id, models.Game.userId == current_user.id)).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    board = [ [ '.' for _ in range(3) ] for _ in range(3) ]
    for move in game.moves:
        board[move.y][move.x] = "X" if move.player == 0 else "O"
    return board


@router.post("/", response_model=schemas.Game)
async def create_game(
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(get_current_user),
    ):
    game = models.Game(finished=False, userId = current_user.id)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

@router.post(
    "/{id}/moves",
    response_model=schemas.Game,
    responses={
        403: {"description": "Operation forbidden"},
        409: {"description": "Conflict"},
    },
)
async def make_move(
        id: str, 
        move: schemas.MoveBase, 
        db: Session = Depends(get_db),
        current_user: schemas.TokenData = Depends(get_current_user),
    ):
    game = db.query(models.Game).filter(and_(models.Game.id == id, models.Game.userId == current_user.id)).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.finished:
        raise HTTPException(
            status_code=403, detail="Game has ended, no more moves allowed")
    if len(game.moves) > 0 and game.moves[-1].player == 0:
        raise HTTPException(
            status_code=403, detail="Not this player's turn")
    if len([past_move for past_move in game.moves if past_move.x == move.x and past_move.y == move.y]) > 0:
        raise HTTPException(
            status_code=409, detail="Position already taken")
    
    db_move = models.Move(**move.model_dump(), player=0, gameId=id)
    db.add(db_move)
    db.flush()
    db.refresh(game)
    ended, winner = gameEnded(game)
    if not ended:
        possible_x = [x for x in range(3) if not sum([move.x == x for move in game.moves]) > 2]
        x = random.choice(possible_x)
        possible_y = [y for y in range(3) if not sum([move.x == x and move.y == y for move in game.moves]) > 0]
        y = random.choice(possible_y)
        db_move = models.Move(x=x, y=y, player=1, gameId=id)
        db.add(db_move)
        db.flush()
        db.refresh(game)
        ended, winner = gameEnded(game)
    if ended:
        game.finished = True
        game.winner = winner
    db.commit()
    db.refresh(game)
    return game