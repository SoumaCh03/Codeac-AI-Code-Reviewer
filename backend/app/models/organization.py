import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.models.base import Base

class Organization(Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    github_installation_id: Mapped[int | None] = mapped_column(index=True, unique=True)
    billing_plan: Mapped[str] = mapped_column(String, default="free")
    
    users = relationship("OrganizationUser", back_populates="organization")
    repositories = relationship("Repository", back_populates="organization")

class OrganizationUser(Base):
    __tablename__ = "organization_users"

    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String, default="member")  # owner, admin, member

    organization = relationship("Organization", back_populates="users")
    user = relationship("User", back_populates="organizations")
