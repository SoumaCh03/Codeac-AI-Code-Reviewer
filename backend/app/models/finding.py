import uuid

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Finding(Base):
    __tablename__ = "findings"

    review_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("review_sessions.id", ondelete="CASCADE")
    )

    rule_id: Mapped[str] = mapped_column(String, index=True)
    # critical, high, medium, low, info
    severity: Mapped[str] = mapped_column(String)
    # security, performance, maintainability, bug
    category: Mapped[str] = mapped_column(String)

    file_path: Mapped[str] = mapped_column(String)
    line_start: Mapped[int | None] = mapped_column(Integer)
    line_end: Mapped[int | None] = mapped_column(Integer)

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    suggestion: Mapped[str | None] = mapped_column(Text)

    confidence_score: Mapped[float | None] = mapped_column(Float)

    status: Mapped[str] = mapped_column(
        String, default="open"
    )  # open, resolved, false_positive

    review_session = relationship("ReviewSession", back_populates="findings")
