'''setup database connection with sqlalchemy to neondb'''

from dotenv import load_dotenv
import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession    
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

ssl_context = ssl.create_default_context()

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context},
    echo=True
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine, 
    class_=AsyncSession
    )

Base = declarative_base()

