import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "localhost"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8080"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "API"
    
    # Auth - API Key
    API_KEY_NAME: str = "access_token"
    API_KEY: Optional[str] = "test"
    COOKIE_DOMAIN: str = "localhost"

    # Auth - Basic
    BASIC_AUTH_USERNAME: str = "john"
    BASIC_AUTH_PASSWORD: str = "doe"

    # Auth - Oauth2
    OAUTH2_USERNAME: str = "john"
    OAUTH2_PASSWORD: str = "doe"
    

    USER_TEST_FULLNAME: str = "Test"
    USER_TEST_EMAIL: EmailStr = "test@bspauto.fr"
    USER_TEST_PASSWORD: str = "test"

    USER_ADMIN_FULLNAME: str = "Admin"
    USER_ADMIN_EMAIL: EmailStr = "admin@bspauto.fr"
    USER_ADMIN_PASSWORD: str = "admin"

    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
