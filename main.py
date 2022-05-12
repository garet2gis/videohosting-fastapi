from api import video_router

from db import database

from fastapi import FastAPI

app = FastAPI()

# metadata.create_all(engine)
app.state.database = database


@app.on_event('startup')
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(video_router)
