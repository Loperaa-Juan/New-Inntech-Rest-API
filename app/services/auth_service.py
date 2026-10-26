import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Cargamos las variables de entorno
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Si falta alguna variable fallamos al arrancar, en lugar de responder 500 en cada login
_missing = [
    name
    for name, value in (
        ("JWT_SECRET_KEY", JWT_SECRET_KEY),
        ("ADMIN_USERNAME", ADMIN_USERNAME),
        ("ADMIN_PASSWORD", ADMIN_PASSWORD),
    )
    if not value
]
if _missing:
    raise RuntimeError(f"Faltan variables de entorno: {', '.join(_missing)}")

# Le indica a Swagger dónde pedir el token (botón "Authorize" en /docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def _unauthorized(detail: str):
    return HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(subject: str):
    expire = datetime.now(timezone.UTC) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def login(username: str, password: str):
    # compare_digest tarda lo mismo acierte o no, así no se pueden adivinar las credenciales midiendo tiempos
    is_valid_username = secrets.compare_digest(
        username.encode(), ADMIN_USERNAME.encode()
    )
    is_valid_password = secrets.compare_digest(
        password.encode(), ADMIN_PASSWORD.encode()
    )

    if not (is_valid_username and is_valid_password):
        raise _unauthorized("Usuario o contraseña incorrectos")

    return {"access_token": create_access_token(username), "token_type": "bearer"}


def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except jwt.ExpiredSignatureError:
        raise _unauthorized("El token expiró")
    except jwt.InvalidTokenError:
        raise _unauthorized("Token inválido")

    if payload["sub"] != ADMIN_USERNAME:
        raise _unauthorized("Token inválido")

    return payload["sub"]
