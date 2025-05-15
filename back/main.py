from fastapi import Depends, FastAPI, BackgroundTasks
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from db import get_db
from crud import *
from schema import WebsiteCreate  
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

class WebsiteUpdate(BaseModel):
    name: str = None
    url: str = None
    interval: int = None
    status: bool = None

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}

@app.get("/test-db")
async def test_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"success": result.scalar() == 1}


@app.post("/websites/")
async def add_website(website: WebsiteCreate, session: AsyncSession = Depends(get_db)):
    website_data = await create_website(
        session, 
        name=website.name, 
        url=website.url, 
        interval=website.interval
    )
    return website_data

@app.get("/websites/")
async def list_websites(session: AsyncSession = Depends(get_db)):
    websites = await get_websites(session)
    return websites

@app.delete("/websites/{website_id}")
async def delete_website_route(website_id: int, session: AsyncSession = Depends(get_db)):
    try:
        result = await delete_website(session, website_id)
        return result
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Website with id {website_id} not found")

@app.put("/websites/{website_id}")
async def update_website_route(website_id: int, website: WebsiteUpdate, session: AsyncSession = Depends(get_db)):
    try:
        updated_website = await update_website(
            session,
            website_id,
            name=website.name,
            url=website.url,
            interval=website.interval,
            status=website.status
        )
        return updated_website
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Website with id {website_id} not found")

