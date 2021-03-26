from fastapi import APIRouter

from app.api.endpoints import home
from app.api.endpoints import basic, apikey, oauth2


api_router = APIRouter()
api_router.include_router(home.router, prefix="", tags=["home"])
api_router.include_router(basic.router, prefix="/basic", tags=["auth basic"])
api_router.include_router(apikey.router, prefix="/apikey", tags=["auth apikey"])
api_router.include_router(oauth2.router, prefix="/oauth2", tags=["auth oauth2"])
