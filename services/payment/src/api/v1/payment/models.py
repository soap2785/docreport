from pydantic import Field, BaseModel, EmailStr


class PaymentSchema(BaseModel):
    summa: int = Field()
    currency: int = Field()
    id: int = Field()
    surname: str = Field()
    name: str = Field()
    patronymic: str = Field()
    email: EmailStr = Field()
    testing: bool = Field(default=False)
    from_bot: bool = Field(default=False)
