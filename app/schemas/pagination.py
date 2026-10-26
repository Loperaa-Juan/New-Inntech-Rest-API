from typing import Generic, TypeVar

import pydantic as _pydantic

T = TypeVar("T")


class PaginationParams(_pydantic.BaseModel):
    skip: int = _pydantic.Field(default=0, ge=0)
    # Tope para que nadie pueda pedir la tabla completa de una vez
    limit: int = _pydantic.Field(default=20, ge=1, le=100)


class Page(_pydantic.BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int
