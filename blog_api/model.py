from typing import Optional

from sqlmodel import SQLModel, Field


class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str