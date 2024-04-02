from fastapi import FastAPI

from app.routers import games, users

with open('./docs/API.md', 'r') as file:
    description = file.read().replace('http://127.0.0.1:8000/docs', '')

app = FastAPI(
    title="Noughts and Crosses",
    description=description,
    summary="Tic-tac-toe (American English), noughts and crosses (British English) is a game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a diagonal, horizontal, or vertical row is the winner.",
)
app.include_router(games.router)
app.include_router(users.router)

@app.get("/")
async def status():
    return {"status": "OK"}
