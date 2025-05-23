# app/schemas/sitecheck.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SiteCheckOut(BaseModel):
    site_id: int
    timestamp: datetime
    status_code: Optional[int]
    response_time_ms: Optional[int]
    ping_ms: Optional[int]
    dns_ms: Optional[int]
    tls_handshake_ms: Optional[int]
    cert_expires_at: Optional[datetime]
    content_length: Optional[int]
    content_type: Optional[str]
    redirect_count: Optional[int]
    http_version: Optional[str]
    up: Optional[bool]
    error_message: Optional[str]
    tls_version: Optional[str]
    cipher_suite: Optional[str]
    mixed_content: Optional[bool]

    class Config:
        from_attributes = True
