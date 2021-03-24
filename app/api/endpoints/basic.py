from fastapi import APIRouter, Depends, Response, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.responses import RedirectResponse

import secrets

from app.core.config import settings


router = APIRouter()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.BASIC_AUTH_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.BASIC_AUTH_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/items")
def read_items(
    username: str = Depends(get_current_username)
):
    return {"items": ["All", "my", "items"]}
