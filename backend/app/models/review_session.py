import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ReviewSession(Base):
    __tablename__ = "review_sessions"

    pull_request_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pull_requests.id", ondelete="CASCADE")
    )
    head_sha: Mapped[str] = mapped_column(String)
    # pending, in_progress, completed, failed
    status: Mapped[str] = mapped_column(String, default="pending")

    pull_request = relationship("PullRequest", back_populates="review_sessions")
    findings = relationship("Finding", back_populates="review_session")
