from sqlalchemy import create_engine
from celery_app import Base
from models import WebsiteCheckResult

DATABASE_URL = 'postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db'  # URL synchrone

engine = create_engine(DATABASE_URL)

# Crée les tables
Base.metadata.create_all(engine)