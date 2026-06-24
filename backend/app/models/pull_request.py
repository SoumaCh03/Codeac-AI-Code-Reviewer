import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, JSON
from app.models.base import Base

class PullRequest(Base):
    __tablename__ = "pull_requests"

    repository_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String) # open, closed, merged
    author_login: Mapped[str] = mapped_column(String)
    base_sha: Mapped[str] = mapped_column(String)
    head_sha: Mapped[str] = mapped_column(String)
    
    repository = relationship("Repository", back_populates="pull_requests")
    review_sessions = relationship("ReviewSession", back_populates="pull_request")
