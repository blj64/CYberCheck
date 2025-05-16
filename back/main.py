from fastapi import Depends, FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from db import get_db
from crud import *
from schema import WebsiteCreate  
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from websocket_manager import manager  # Import the manager from the new module

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class WebsiteUpdate(BaseModel):
    name: str = None
    url: str = None
    interval: int = None
    status: bool = None

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

@app.websocket("/ws/website/{website_id}")
async def websocket_endpoint(websocket: WebSocket, website_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

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

@app.get("/websites/{website_id}/details")
async def get_website_details(website_id: int, session: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    from sqlalchemy.orm import joinedload
    from models import Website, WebsiteCheckResult

    website = await session.get(Website, website_id)
    if not website:
        raise HTTPException(status_code=404, detail=f"Website with id {website_id} not found")

    # Fetch the latest check result for the website
    result = await session.execute(
        select(WebsiteCheckResult)
        .where(WebsiteCheckResult.website_id == website_id)
        .order_by(WebsiteCheckResult.checked_at.desc())  # Order by the most recent
        .limit(1)  # Fetch only the latest log
    )
    latest_check_result = result.scalar()

    return {
        "website": website,
        "latest_check_result": latest_check_result,
    }

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

