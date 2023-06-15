from pydantic import BaseSettings, AnyHttpUrl, validator, HttpUrl, EmailStr, AnyUrl
import secrets
from typing import Any, Dict, List, Optional, Union

class Settings(BaseSettings):
    #! Database
    MYSQL_USER: str = "admin"
    MYSQL_PASSWORD: str = "XiLcg8r4"
    MYSQL_HOST: str = "mysql-131853-0.cloudclusters.net"
    MYSQL_PORT: str = "15638"
    MYSQL_DB: str = "Rayotec"
    SQLALCHEMY_DATABASE_URI: Optional[AnyUrl] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AnyUrl.build(
            scheme="mysql+mysqlconnector",
            user=values.get("MYSQL_USER"),
            password=values.get("MYSQL_PASSWORD"),
            host=values.get("MYSQL_HOST"),
            port=values.get("MYSQL_PORT"),
            path=f"/{values.get('MYSQL_DB')}",
        )
    
    #! Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    #! API
    SERVER_NAME: str = "Railway"
    PROJECT_NAME: str = "Rayotec"
    PROJECT_DESCRIPTION: str = "API para el *Sistema de Gestión de Rayotec*\n\n<h2>Documentación</h2>\n<p>Para ver la documentación de la API, ingrese a la siguiente URL:</p>\n<a href='https://rayotec.up.railway.app/redoc'>/redoc</a>\n"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    ALLOWED_HOSTS: List[str] = ["*"]
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def get_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    #! Email
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp-mail.outlook.com"
    SMTP_USER: str = "rayotec.store@hotmail.com"
    SMTP_PASSWORD: str = "qwer123er"
    
    class Config:
        case_sensitive = True

settings = Settings()

    
