from pydantic import BaseModel

class WebsiteSearchRequest(BaseModel):
    query: str
    limit: int = 10
