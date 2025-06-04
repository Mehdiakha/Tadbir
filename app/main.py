from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from .utils.auth import hash_password
from .schemas import UserCreate, UserOut

from .models import User, Base
from .database import engine, SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run this on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Optionally: cleanup here on shutdown

app = FastAPI(lifespan=lifespan)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.post("/users/")
async def create_user(user: UserCreate ,db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User created"}

@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user