from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from .utils.auth import hash_password

from . import models
from .database import engine, SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run this on startup
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # Optionally: cleanup here on shutdown

app = FastAPI(lifespan=lifespan)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/users/")
async def create_user(db: AsyncSession = Depends(get_db)):
    new_user = models.User(
        username="mehdi",
        email="mehdi@example.com",
        hashed_password=hash_password("your_plain_password")
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User created"}

@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users
