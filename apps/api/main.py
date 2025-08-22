import os
from fastapi import FastAPI
from .api import router
from .deps import engine
from . import models
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Desi Holmes API", version="0.2.0")
app.include_router(router)

@app.on_event("startup")
def startup():
    # ensure tables exist
    models.Base.metadata.create_all(bind=engine)
