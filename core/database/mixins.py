from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedUpdatedMixin:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime | None] = mapped_column(default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(
        default=func.now(), onupdate=datetime.utcnow
    )
