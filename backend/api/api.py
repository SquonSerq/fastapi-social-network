from fastapi import APIRouter

from .endpoints import login, users, posts, likes_dislikes

api_router = APIRouter()
api_router.include_router(login.router, tags=['login'])
api_router.include_router(users.router, tags=['users'])
api_router.include_router(posts.router, tags=['posts'])
api_router.include_router(likes_dislikes.router, tags=['likes and dislikes'])
