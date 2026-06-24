from fastapi import APIRouter

from app.api.api_v1.endpoints import github, repos

api_router = APIRouter()
api_router.include_router(github.router, prefix="/github", tags=["github"])
api_router.include_router(repos.router, prefix="/repos", tags=["repos"])
