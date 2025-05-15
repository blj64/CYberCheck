from pydantic import BaseModel, HttpUrl

class WebsiteCreate(BaseModel):
    name: str
    url: HttpUrl
    interval: int
    status: bool = True
