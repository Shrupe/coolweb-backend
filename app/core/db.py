from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import DATABASE_URL

# DATABASE_URL should be in async format: postgresql+asyncpg://user:pass@host/db
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
                        bind=engine, 
                        class_=AsyncSession, 
                        expire_on_commit=False
                        )
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session