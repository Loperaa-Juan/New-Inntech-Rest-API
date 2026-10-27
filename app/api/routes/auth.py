from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...schemas import Token as _token
from ...schemas import errors as _errors
from ...services import auth_service as _authServices

router = APIRouter()


@router.post(
    "/token",
    response_model=_token.Token,
    responses={401: _errors.error_response("Usuario o contraseña incorrectos")},
)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Recibe `username` y `password` como formulario (application/x-www-form-urlencoded) y devuelve un token JWT.
    """
    return _authServices.login(form_data.username, form_data.password)
