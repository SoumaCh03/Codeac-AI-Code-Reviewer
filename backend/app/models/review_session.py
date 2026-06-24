import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.models.base import Base

class ReviewSession(Base):
    __tablename__ = "review_sessions"

    pull_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("pull_requests.id", ondelete="CASCADE"))
    head_sha: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, in_progress, completed, failed
    
    pull_request = relationship("PullRequest", back_populates="review_sessions")
    findings = relationship("Finding", back_populates="review_session")
