import asyncio
import logging
import aiomysql
from app.infrastructure.config.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

async def wait_for_db(retries=10, delay=5):
    for attempt in range(retries):
        try:
            connection = await aiomysql.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                charset='utf8mb4',
                connect_timeout=30,
                autocommit=True,
                program_name='editor_voz_app'
            )
            return connection
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{retries} failed: {str(e)}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
    raise Exception("Could not connect to database after maximum retries")

async def create_database():
    connection = None
    try:
        connection = await wait_for_db()
        async with connection.cursor() as cursor:
            # Crear base de datos
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}`")
            await cursor.execute(f"USE `{settings.DB_NAME}`")
            
            # Crear tabla users
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # Crear tabla documents
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    user_id INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            await connection.commit()
            logger.info("Database and tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    asyncio.run(create_database())