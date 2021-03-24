from fastapi import APIRouter, Depends, Response, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

from starlette.responses import RedirectResponse

from app.core.config import settings


router = APIRouter()


api_key_query = APIKeyQuery(name=settings.API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=settings.API_KEY_NAME, auto_error=False)


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == settings.API_KEY:
        return api_key_query
    elif api_key_header == settings.API_KEY:
        return api_key_header
    elif api_key_cookie == settings.API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        )


@router.post("/setCookie")
def set_cookie(
    response: Response
):
    response.set_cookie(
        settings.API_KEY_NAME,
        value=settings.API_KEY,
        domain=settings.COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return {"message": "Cookie set"}


@router.get("/items")
def read_items(
    api_key: APIKey = Depends(get_api_key)
):
    response = "These are all my items."
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url=settings.API_V1_STR)
    response.delete_cookie(settings.API_KEY_NAME, domain=settings.COOKIE_DOMAIN)
    return response
