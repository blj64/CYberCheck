from celery import Celery
from celery.schedules import crontab
import httpx
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
from models import Website, WebsiteCheckResult
from ping3 import ping
from urllib.parse import urlparse
from crud import save_website_check_result
from sqlalchemy.orm import sessionmaker
import asyncio
from fastapi.websockets import WebSocket
from websocket_manager import manager  # Import the manager from websocket_manager.py


celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",  # URL de connexion à Redis
)

celery_app.conf.beat_schedule = {
    "check-websites-every-minute": {
        "task": "celery_app.schedule_website_checks",
        "schedule": crontab(minute="*"),  # Exécuter toutes les minutes
    },
}


DATABASE_URL = "postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task
def check_website_status(website_id: int, url: str):
    from datetime import datetime
    from urllib.parse import urlparse
    import httpx
    from ping3 import ping

    session = SessionLocal()

    try:
        response = httpx.get(url, timeout=10, follow_redirects=True)
        status_code = response.status_code
        hostname = urlparse(url).hostname
        ping_ms = None
        if hostname:
            ping_ms = ping(hostname, timeout=3)

        result_data = WebsiteCheckResult(
            website_id=website_id,
            status_code=status_code,
            speed_bps=len(response.content),
            ping=int(ping_ms * 1000) if ping_ms else None,
            cert_expire=None,
            cert_expired=None,
            cert_error=None,
            checked_at=datetime.utcnow(),
        )

        session.add(result_data)
        session.commit()

        # Broadcast the new log to WebSocket clients
        asyncio.run(broadcast_update(website_id, {
            "website_id": website_id,
            "status_code": status_code,
            "ping": int(ping_ms * 1000) if ping_ms else None,
            "checked_at": datetime.utcnow().isoformat(),
        }))
    except Exception as e:
        print(f"[ERROR] Could not check {url}: {e}")
        session.rollback()
    finally:
        session.close()

async def broadcast_update(website_id: int, data: dict):
    await manager.broadcast(data)  # Use the manager from websocket_manager.py

@celery_app.task
def schedule_website_checks():
    from sqlalchemy.future import select
    import asyncio

    async def fetch_websites():
        try:
            async with async_session() as session:
                result = await session.execute(select(Website))
                websites = result.scalars().all()
                if not websites:
                    print("No websites found to check.")
                    return {"message": "No websites found"}
                scheduled_websites = []
                for website in websites:
                    print(f"Scheduling check for website: {website.url}")
                    check_website_status.delay(website.id, website.url)
                    scheduled_websites.append(website.url)
                print(f"Scheduled checks for websites: {scheduled_websites}")
                return {"scheduled_websites": scheduled_websites}
        except Exception as e:
            print(f"Error scheduling website checks: {e}")
            raise e

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_websites())


