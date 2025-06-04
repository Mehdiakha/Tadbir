from pydantic import BaseModel, EmailStr
from datetime import datetime

# Incoming user data (for user creation)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Not 'hashed_password' – the raw password from client

# Outgoing user data (API response)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # Allows SQLAlchemy models to be converted to Pydantic
