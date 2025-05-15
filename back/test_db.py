
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = 'postgresql+asyncpg://fastapi_user:fastapi_password@db:5432/fastapi_db'

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.connect() as conn:
        result = await conn.execute('SELECT 1')
        print(result.scalar())

asyncio.run(test_connection())

