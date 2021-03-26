from datetime import datetime, timedelta
from typing import Any
from jose import jwt

from fastapi import APIRouter, Depends, Response, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import settings


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.API_V1_STR+"/oauth2/token")


ALGORITHM = "HS256"


@router.post("/token")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    if form_data.username == settings.OAUTH2_USERNAME and form_data.password == settings.OAUTH2_PASSWORD:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        if access_token_expires:
            expire = datetime.utcnow() + access_token_expires
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": form_data.username}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": encoded_jwt,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token, "items": ["All", "my", "items"]}
