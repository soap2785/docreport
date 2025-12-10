from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(10, le=4)
    offset: int = Field(0, ge=0)
