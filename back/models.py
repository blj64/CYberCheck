from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Interval, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    interval = Column(Interval, nullable=False)  # Intervalle de surveillance
    status = Column(Boolean, default=True)  # Statut du site (actif/inactif)

class WebsiteCheckResult(Base):
    __tablename__ = "website_check_results"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    status_code = Column(Integer, nullable=True)  # Code HTTP retourné
    error = Column(String, nullable=True)  # Message d'erreur, si applicable
    checked_at = Column(DateTime(timezone=True), server_default=func.now())  # Date/heure de la vérification
    speed_bps = Column(Integer, nullable=True)  # Vitesse de téléchargement en Bps
    ping = Column(Integer, nullable=True)  # Temps de ping en ms
    cert_expire = Column(String, nullable=True)  # Date d'expiration du certificat SSL
    cert_expired = Column(Boolean, nullable=True)  # Indique si le certificat est expiré
    cert_error = Column(String, nullable=True)  # Erreur liée au certificat SSL, si applicable