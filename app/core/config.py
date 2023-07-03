from pydantic import BaseSettings, AnyHttpUrl, validator, HttpUrl, EmailStr, AnyUrl
import secrets
from typing import Any, Dict, List, Optional, Union

class Settings(BaseSettings):
    #! Database
    #MYSQL_USER: str = "root"
    MYSQL_USER: str = "admin"
    #MYSQL_PASSWORD: str = "2LP1x6uiKBpaBWCutwNL"
    MYSQL_PASSWORD: str = "adbO1NJG"
    #MYSQL_HOST: str = "containers-us-west-54.railway.app"
    MYSQL_HOST: str = "mysql-43314-0.cloudclusters.net"
    #MYSQL_PORT: str = "7677"
    MYSQL_PORT: str = "19751"
    #MYSQL_DB: str = "railway"
    MYSQL_DB: str = "FlaskBd"
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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 200

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
    
    #! Configuracion SMTP
    """
    Nombre de servidor: smtp.office365.com
    Puerto: 587
    Método de cifrado: STARTTLS
    """
    SMTP_HOST: str = "smtp.office365.com"
    SMTP_PORT: int = 587
    SMTP_TLS: bool = True
    SMTP_USER: str = "rayotec.store@hotmail.com"
    SMTP_PASSWORD: str = "qwer123er"
    
    class Config:
        case_sensitive = True

settings = Settings()