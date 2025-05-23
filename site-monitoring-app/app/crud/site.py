from sqlalchemy.orm import Session
from app.models.site import MonitoredSite, SiteCheck
from app.schemas.site import SiteCreate
from typing import List

def get_site(db: Session, site_id: int) -> MonitoredSite | None:
    return db.query(MonitoredSite).filter(MonitoredSite.id == site_id).first()

def get_sites(db: Session) -> List[MonitoredSite]:
    return db.query(MonitoredSite).all()

def create_site(db: Session, site_in: SiteCreate) -> MonitoredSite:
    data = site_in.dict()
    data["url"] = str(data["url"])
    site = MonitoredSite(**data)
    db.add(site)
    db.commit()
    db.refresh(site)
    return site

def update_site(db: Session, site_id: int, site_in: SiteCreate) -> MonitoredSite:
    site = get_site(db, site_id)
    if not site:
        return None
    # Mets à jour tous les champs
    site.name = site_in.name
    site.url = str(site_in.url)
    site.delay_seconds = site_in.delay_seconds
    db.commit()
    db.refresh(site)
    return site

def delete_site(db: Session, site_id: int) -> bool:
    site = db.query(MonitoredSite).filter(MonitoredSite.id == site_id).first()
    if not site:
        return False

    # 1) supprimer les checks associés
    db.query(SiteCheck).filter(SiteCheck.site_id == site_id).delete()

    # 2) supprimer le site
    db.delete(site)
    db.commit()
    return True

def delete_checks_for_site(db: Session, site_id: int):
    db.query(SiteCheck).filter(SiteCheck.site_id == site_id).delete()
    db.commit()

def get_checks(db, site_id, limit):
    return db.query(SiteCheck).filter_by(site_id=site_id) \
             .order_by(SiteCheck.timestamp.desc()).limit(limit).all()
