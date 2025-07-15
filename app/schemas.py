from pydantic import BaseModel

class URLCreate(BaseModel):
    original_url: str

class URLInfo(BaseModel):
    short_url: str
