from fastapi import FastAPI

from .database import Base, engine

from . import models

from .routes import user, task


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(user.router)

app.include_router(task.router)


@app.get("/")

def home():

    return {"message": "API working"}