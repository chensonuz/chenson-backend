from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database.db import Base
from core.database.mixins import CreatedUpdatedMixin


class AddressInfo(Base, CreatedUpdatedMixin):
    __tablename__ = "addresses_info"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    address: Mapped[str]
    location: Mapped[str]
    apartment: Mapped[str] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)
    entrance: Mapped[str] = mapped_column(nullable=True)
    floor: Mapped[str] = mapped_column(nullable=True)
