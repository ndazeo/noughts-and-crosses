from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    finished = Column(Boolean)
    winner = Column(Integer, nullable=True)
    moves = relationship("Move", back_populates="game")


class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True)
    gameId = Column(Integer, ForeignKey("games.id"))
    player = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    
    game = relationship("Game", back_populates="moves")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)