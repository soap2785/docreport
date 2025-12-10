from pydantic import Field, BaseModel
from datetime import date


class SubmitRequestSchema(BaseModel):
    id: int = Field()

    fullname: str = Field(max_length=128)
    region: str | None = Field(default=None, max_length=64)

    birthdate: date | None = Field(default=None)
    passport_date: date | None = Field(default=None)

    passport_series: str | None = Field(default=None)
    passport_number: str | None = Field(default=None)

    state: bool | None = Field(default=False)


class RequestSchema(SubmitRequestSchema):
    id: int


class BotPayload:
    fullname: str
    region: str
    birthdate: str
    passport: str
    passportDate: str


class ResponseData:
    inn: int | None = None
    fns: str = 'Данные не обнаружены'
    ter: str = 'Данные не обнаружены'
    civ: list | str = 'Данные не обнаружены'
    bank: dict | str = 'Данные не обнаружены'
    iss: list | str = 'Данные не обнаружены'
    warnip: list | str = 'Данные не обнаружены'
    warnorg: list | str = 'Данные не обнаружены'
    warnuchr1: list | str = 'Данные не обнаружены'
    warnuchr2: list | str = 'Данные не обнаружены'
    disq: dict | str = 'Данные не обнаружены'
    semp: str = 'Данные не обнаружены'
    inter: str = 'Данные не обнаружены'
    mass: str = 'Данные не обнаружены'
    arb: list | str = 'Данные не обнаружены'
    org: list | str = 'Данные не обнаружены'
    law: list | str = 'Данные не обнаружены'
    vk: list | str = 'Данные не обнаружены'
    ok: list | str = 'Данные не обнаружены'


class Response(BaseModel):
    response_data_dict: dict = Field()
