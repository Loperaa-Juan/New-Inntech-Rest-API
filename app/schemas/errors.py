import pydantic as _pydantic


# Misma forma que el cuerpo de un HTTPException
class ErrorMessage(_pydantic.BaseModel):
    detail: str


def error_response(description: str):
    """Documenta en Swagger una respuesta de error con su motivo."""
    return {"model": ErrorMessage, "description": description}


# Respuesta común de las rutas protegidas con el token del administrador
UNAUTHORIZED = {401: error_response("Falta el token, está vencido o es inválido")}
