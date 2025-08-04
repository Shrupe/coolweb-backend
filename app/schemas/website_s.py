from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from pydantic import ConfigDict  

class WebsiteBase(BaseModel):
    name: str
    url: HttpUrl
    description: str
    tags: List[str] = []
    screenshot_url: Optional[HttpUrl] = None

class WebsiteCreate(WebsiteBase):
    pass

class WebsiteRead(WebsiteBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  

class WebsiteListResponse(BaseModel):
    total: int
    items: List[WebsiteRead]

class WebsiteSearchRequest(BaseModel):
    query: str
