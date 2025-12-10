from pydantic import Field, BaseModel
from datetime import date


class CreateUpdateRequestSchema(BaseModel):
    id: int | None = Field(default=None)

    fullname: str = Field(max_length=128)
    region: str | None = Field(default=None, max_length=64)

    birthdate: date | None = Field(default=None)
    passport_date: date | None = Field(default=None)

    passport_series: str | None = Field(default=None)
    passport_number: str | None = Field(default=None)

    state: bool | None = Field(default=False)


class RequestSchema(CreateUpdateRequestSchema):
    id: int
