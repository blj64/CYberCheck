import datetime
import subprocess as _subprocess  # underscore pour éviter tout écrasement
import socket
import ssl
from urllib.parse import urlparse
import requests
import time
import re
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.site import MonitoredSite, SiteCheck
from app.websocket.notifier import manager

scheduler = BackgroundScheduler()



def check_site(site_id: int, url: str):
    db = SessionLocal()
    parsed = urlparse(url)
    host = parsed.hostname

    # 1) HTTP GET
    try:
        t0 = time.time()
        resp = requests.get(url, timeout=5)
        response_time_ms = int((time.time() - t0) * 1000)
        status_code = resp.status_code
        error_http = None
    except Exception as e:
        resp = None
        response_time_ms = None
        status_code = None
        error_http = f"HTTP:{e}"

    # 2) DNS lookup
    try:
        t0 = time.time()
        socket.getaddrinfo(host, None)
        dns_ms = int((time.time() - t0) * 1000)
        error_dns = None
    except Exception as e:
        dns_ms = None
        error_dns = f"DNS:{e}"

    # 3) TLS handshake & cert
    try:
        t0 = time.time()
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(5)
            s.connect((host, 443))
            cert = s.getpeercert()
            cipher_info = s.cipher()  # (cipher, version, bits)
        tls_handshake_ms = int((time.time() - t0) * 1000)
        tls_version = cipher_info[1]
        cipher_suite = cipher_info[0]
        cert_expires_at = datetime.datetime.strptime(
            cert['notAfter'], '%b %d %H:%M:%S %Y %Z'
        )
        error_tls = None
    except Exception as e:
        tls_handshake_ms = None
        tls_version = None
        cipher_suite = None
        cert_expires_at = None
        error_tls = f"TLS:{e}"

    # 4) ICMP ping
    try:
        out = _subprocess.run(
            ['ping', '-c', '1', '-W', '1', host],
            capture_output=True, text=True, check=True
        ).stdout
        ping_ms = int(float(out.split('time=')[1].split()[0]))
        error_ping = None
    except Exception as e:
        ping_ms = None
        error_ping = f"PING:{e}"

    # 5) Mixed content check
    if resp and resp.content:
        mixed_content = bool(re.search(b"href=[\"']http://", resp.content, re.IGNORECASE))
    else:
        mixed_content = None

    # 6) Other HTTP metrics
    content_length = len(resp.content) if resp and resp.content is not None else None
    content_type = resp.headers.get('Content-Type') if resp else None
    redirect_count = len(resp.history) if resp else 0
    http_version = None
    if resp and hasattr(resp.raw, 'version'):
        http_version = '2' if resp.raw.version == 2 else '1.1'
    up = status_code is not None and 200 <= status_code < 300

    # Consolidate errors
    error_message = '; '.join(filter(None, [error_http, error_dns, error_tls, error_ping])) or None

    # Persist in DB
    check = SiteCheck(
        site_id=site_id,
        status_code=status_code,
        response_time_ms=response_time_ms,
        ping_ms=ping_ms,
        dns_ms=dns_ms,
        tls_handshake_ms=tls_handshake_ms,
        tls_version=tls_version,
        cipher_suite=cipher_suite,
        cert_expires_at=cert_expires_at,
        content_length=content_length,
        content_type=content_type,
        redirect_count=redirect_count,
        http_version=http_version,
        up=up,
        mixed_content=mixed_content,
        error_message=error_message
    )
    db.add(check)
    db.commit()
    db.close()

    # Broadcast via WebSocket
    payload = {
        'site_id': site_id,
        'status_code': status_code,
        'response_time_ms': response_time_ms,
        'ping_ms': ping_ms,
        'dns_ms': dns_ms,
        'tls_handshake_ms': tls_handshake_ms,
        'tls_version': tls_version,
        'cipher_suite': cipher_suite,
        'cert_expires_at': cert_expires_at.isoformat() if cert_expires_at else None,
        'content_length': content_length,
        'content_type': content_type,
        'redirect_count': redirect_count,
        'http_version': http_version,
        'up': up,
        'mixed_content': mixed_content,
        'error_message': error_message,
    }
    if manager.loop:
        asyncio.run_coroutine_threadsafe(manager.broadcast(payload), manager.loop)
        
def load_jobs():
    db = SessionLocal()
    sites = db.query(MonitoredSite).all()
    for s in sites:
        scheduler.add_job(
            check_site,
            'interval',
            seconds=s.delay_seconds,
            args=[s.id, s.url],
            id=f"site-{s.id}",
            replace_existing=True
        )
    db.close()

def start_scheduler():
    if scheduler.state != 1:
        load_jobs()
        scheduler.start()
