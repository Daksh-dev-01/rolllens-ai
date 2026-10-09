from typing import Any
from pydantic import BaseModel
class Success(BaseModel):
    success: bool = True
    data: Any
class ErrorBody(BaseModel):
    success: bool = False
    error: dict[str, Any]
