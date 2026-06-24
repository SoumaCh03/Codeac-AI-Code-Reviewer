from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.api import deps
from app.models.user import User
from app.models.repository import Repository
from app.core.database import get_db

router = APIRouter()


@router.get("/")
def read_repositories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Basic implementation, should filter by organization in production
    repos = db.query(Repository).offset(skip).limit(limit).all()
    return repos
