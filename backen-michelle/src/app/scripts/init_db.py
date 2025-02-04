import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from infrastructure.config.settings import get_settings
from infrastructure.database.connection import DATABASE_URL
from domain.models.user import User
from domain.models.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_database():
    settings = get_settings()
    
    # Crear engine sin base de datos
    engine = create_async_engine(
        f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}",
        echo=True
    )
    
    async with engine.connect() as conn:
        # Crear base de datos si no existe
        await conn.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}")
        await conn.execute(f"USE {settings.DB_NAME}")
        
        # Crear tablas
        async with create_async_engine(DATABASE_URL).begin() as conn:
            await conn.run_sync(User.metadata.create_all)
            await conn.run_sync(Document.metadata.create_all)
            
    logger.info("Database and tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_database())