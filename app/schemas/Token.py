import pydantic as _pydantic


class Token(_pydantic.BaseModel):
    access_token: str
    token_type: str
