from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401  (importing registers the tables)
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="PetCare Hub API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}