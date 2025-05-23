import asyncio
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy.exc import OperationalError
from app.database import engine, Base
from app.workers.checker import start_scheduler
from app.websocket.notifier import manager
from app.router.site_router import router as site_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # port de ton front Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
async def wait_for_db(max_retries: int = 20, delay: float = 1.0):
    """
    Tente de se connecter à la base jusqu'à réussite ou après max_retries.
    """
    for attempt in range(1, max_retries + 1):
        try:
            conn = engine.connect()
            conn.close()
            print(f"[MAIN] DB prête (tentative {attempt})")
            return
        except OperationalError:
            print(f"[MAIN] DB non prête, tentative {attempt}/{max_retries}…")
            await asyncio.sleep(delay)
    raise RuntimeError("Impossible de joindre la base de données après plusieurs essais")

@app.on_event("startup")
async def on_startup():
    # 1) on attend vraiment la BDD
    await wait_for_db()

    # 2) on crée les tables
    print("[MAIN] Création des tables")
    Base.metadata.create_all(bind=engine)

    # 3) on capture la loop pour le WebSocket
    manager.loop = asyncio.get_event_loop()
    print("[MAIN] Loop capturée, démarrage du scheduler")

    # 4) on démarre APScheduler
    start_scheduler()

# Router pour l'API REST
app.include_router(site_router)

# Endpoint WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # pour garder la connexion ouverte
    except WebSocketDisconnect:
        manager.disconnect(websocket)
