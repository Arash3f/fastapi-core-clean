from typing import Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

from app.domain.exceptions.common_exceptions import (
    InvalidPageException,
    InvalidPageSizeException,
)

T = TypeVar("T")


class PaginatedResult(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @model_validator(mode="after")
    def validate_pagination(self) -> "PaginationParams":
        if self.page < 1:
            raise InvalidPageException()
        if self.page_size < 1:
            raise InvalidPageSizeException()
        return self
