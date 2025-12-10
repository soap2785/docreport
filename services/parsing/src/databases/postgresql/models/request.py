from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Boolean
from datetime import date

from ..base import Base


class Request(Base):
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(primary_key=True)

    fullname: Mapped[str] = mapped_column(String(128), nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String(64))

    birthdate: Mapped[Optional[date]] = mapped_column(Date())
    passport_date: Mapped[Optional[date]] = mapped_column(Date())

    passport_series: Mapped[Optional[str]] = mapped_column(String(4))
    passport_number: Mapped[Optional[str]] = mapped_column(String(6))

    state: Mapped[bool] = mapped_column(Boolean())
