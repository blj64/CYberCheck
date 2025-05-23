from pydantic import BaseModel, HttpUrl
from typing import Optional

class SiteBase(BaseModel):
    name: str
    url: HttpUrl
    delay_seconds: int

class SiteCreate(SiteBase):
    pass

class SiteInDB(SiteBase):
    id: int

    class Config:
        orm_mode = True


