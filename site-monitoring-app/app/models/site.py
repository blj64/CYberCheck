from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class MonitoredSite(Base):
    __tablename__ = "monitored_sites"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String, nullable=False)
    url            = Column(String, nullable=False)
    delay_seconds  = Column(Integer, nullable=False)

class SiteCheck(Base):
    __tablename__ = 'site_checks'
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    ping_ms = Column(Integer)
    dns_ms = Column(Integer)
    tls_handshake_ms = Column(Integer)
    tls_version = Column(String(50))            # nouvelle colonne
    cipher_suite = Column(String(100))          # nouvelle colonne
    cert_expires_at = Column(DateTime(timezone=True))

    content_length = Column(Integer)
    content_type = Column(String(100))
    redirect_count = Column(Integer)
    http_version = Column(String(10))
    up = Column(Boolean, default=False)
    mixed_content = Column(Boolean)             # nouvelle colonne
    error_message = Column(Text)