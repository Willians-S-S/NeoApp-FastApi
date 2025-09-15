from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Número da página")
    size: int = Field(default=10, ge=1, le=100, description="Itens por página")
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

class PageResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int):
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=ceil(total / size) if size > 0 else 0
        )
