from fastapi import APIRouter
from app.api.v1 import auth, appeals, users, departments, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(appeals.router, prefix="/appeals", tags=["appeals"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
