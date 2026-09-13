from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SortOrderField(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortParams(BaseModel, Generic[T]):
    sort_by: T
    sort_order: SortOrderField = SortOrderField.ASC
