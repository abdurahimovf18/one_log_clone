from typing import Generic, TypeVar

from src.core.data_transfer_objects.base import BaseDTO

T = TypeVar("T", bound=BaseDTO)


class PageDTO(BaseDTO, Generic[T]):  # noqa: UP046
    items: list[T]
    page: int
    items_per_page: int
    is_next: bool
    is_prev: bool
    items_count: int
    pages_count: int
