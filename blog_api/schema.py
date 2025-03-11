from typing import Optional

from pydantic import BaseModel


class BlogCreate(BaseModel):
    name: str
    description: str


class BlogUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

