from datetime import timedelta
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from models import Website, WebsiteCheckResult
from db import async_session

async def create_website(session: AsyncSession, name: str, url: str, interval, status: bool = True):
    # Convertir HttpUrl en str si nécessaire
    interval_timedelta = timedelta(seconds=interval)

    if isinstance(url, HttpUrl):
        url = str(url)
    
    website = Website(name=name, url=url, interval=interval_timedelta, status=status)
    session.add(website)
    await session.commit()
    await session.refresh(website)
    return website

async def get_websites(session: AsyncSession):
    result = await session.execute(select(Website))
    return result.scalars().all()

async def delete_website(session: AsyncSession, website_id: int):
    result = await session.execute(select(Website).where(Website.id == website_id))
    website = result.scalars().first()
    if not website:
        raise NoResultFound(f"Website with id {website_id} not found")
    await session.delete(website)
    await session.commit()
    return {"message": f"Website with id {website_id} has been deleted"}

async def update_website(session: AsyncSession, website_id: int, name: str = None, url: str = None, interval: int = None, status: bool = None):
    result = await session.execute(select(Website).where(Website.id == website_id))
    website = result.scalars().first()
    if not website:
        raise NoResultFound(f"Website with id {website_id} not found")
    
    # Mettre à jour les champs si des valeurs sont fournies
    if name is not None:
        website.name = name
    if url is not None:
        website.url = str(url)  # Convertir HttpUrl en str si nécessaire
    if interval is not None:
        from datetime import timedelta
        website.interval = timedelta(seconds=interval)
    if status is not None:
        website.status = status

    session.add(website)
    await session.commit()
    await session.refresh(website)
    return website

async def save_website_check_result(result: dict):
    async with async_session() as session:
        async with session.begin():
            check_result = WebsiteCheckResult(
                website_id=result["website_id"],
                status_code=result.get("status_code"),
                error=result.get("error"),
                speed_bps=result.get("speed_bps"),
                ping=result.get("ping"),
                cert_expire=result.get("cert_expire"),
                cert_expired=result.get("cert_expired"),
                cert_error=result.get("cert_error"),
            )
            session.add(check_result)
        await session.commit()