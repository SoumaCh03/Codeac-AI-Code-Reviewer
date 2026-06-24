import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Repository(Base):
    __tablename__ = "repositories"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE")
    )
    github_id: Mapped[int] = mapped_column(index=True, unique=True)
    full_name: Mapped[str] = mapped_column(String, index=True)  # e.g. owner/repo
    default_branch: Mapped[str] = mapped_column(String, default="main")
    language: Mapped[str | None] = mapped_column(String)

    organization = relationship("Organization", back_populates="repositories")
    pull_requests = relationship("PullRequest", back_populates="repository")
