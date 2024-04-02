from fastapi import FastAPI

from app.routers import games

app = FastAPI()
app.include_router(games.router)

@app.get("/")
async def status():
    return {"status": "OK"}
