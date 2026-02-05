from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserOutput
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB at Start
    print("Creating Tables...")
    time.sleep(8)
    create_tables()
    print("Tables Created.")
    yield # speration point
    

app = FastAPI(lifespan = lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/protected")
def read_protected(user : UserOutput = Depends(get_current_user)):
    return {"data": user}