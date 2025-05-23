from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Response
from app.database import SessionLocal
from app.models.site import MonitoredSite, SiteCheck
from app.schemas.site import SiteCreate, SiteInDB
from app.crud.site import delete_checks_for_site, get_site, get_sites, create_site, update_site, delete_site
from app.workers.checker import scheduler, check_site
from app.schemas.sitecheck import SiteCheckOut 

router = APIRouter(prefix="/sites", tags=["sites"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[SiteInDB])
def read_sites(db: Session = Depends(get_db)):
    return get_sites(db)

@router.get("/{site_id}", response_model=SiteInDB)
def read_site(site_id: int, db: Session = Depends(get_db)):
    site = get_site(db, site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site non trouvé.")
    return site

@router.post("/", response_model=SiteInDB, status_code=status.HTTP_201_CREATED)
def add_site(site_in: SiteCreate, db: Session = Depends(get_db)):
    existing = db.query(MonitoredSite).filter_by(url=str(site_in.url)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un site avec cette URL existe déjà.")
    site = create_site(db, site_in)
    # planifier immédiatement
    scheduler.add_job(
        check_site,
        trigger="interval",
        seconds=site.delay_seconds,
        args=[site.id, site.url],
        id=f"site-{site.id}",
        replace_existing=True
    )
    return site

@router.put("/{site_id}", response_model=SiteInDB)
def edit_site(site_id: int, site_in: SiteCreate, db: Session = Depends(get_db)):
    site = update_site(db, site_id, site_in)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site non trouvé.")
    job_id = f"site-{site_id}"
    if scheduler.get_job(job_id):
        scheduler.reschedule_job(job_id, trigger="interval", seconds=site.delay_seconds)
    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_site(site_id: int, db: Session = Depends(get_db)):
    success = delete_site(db, site_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site non trouvé.")
    job_id = f"site-{site_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    return

@router.get(
    "/{site_id}/checks/",
    response_model=List[SiteCheckOut],
    summary="Récupère les derniers checks d'un site",
)
def read_site_checks(
    site_id: int,
    limit: Optional[int] = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Renvoie les `limit` derniers checks pour un site, triés du plus récent au plus ancien.
    """
    return (
        db.query(SiteCheck)
          .filter(SiteCheck.site_id == site_id)
          .order_by(SiteCheck.timestamp.desc())
          .limit(limit)
          .all()
    )

@router.delete("/{site_id}/checks/", status_code=status.HTTP_204_NO_CONTENT)
def clear_checks(site_id: int, db: Session = Depends(get_db)):
    deleted = delete_checks_for_site(db, site_id)
    if deleted == 0:
        # on peut 404 si on veut, ou simplement renvoyer 204 même si rien à faire
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_204_NO_CONTENT)