from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlalchemy.orm import Session
from typing import Optional

from db.db import get_session
from schemas.user_schemas import UserCreate, UserResponse
from services.user_service import UserService
from schemas.page_schemas import PageResponse, PaginationParams

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code= HTTPStatus.CREATED)
def creat_user(user: UserCreate, db: Session = Depends(get_session)):
    return UserService(db).save(user=user)
 
@router.get("/users/", response_model=PageResponse[UserResponse])
def get_users_paginated(
    page: int = Query(default=1, ge=1, description="Número da página"),
    size: int = Query(default=10, ge=1, le=100, description="Itens por página"),
    order_by: str = Query(default="creat_at", description="Campo para ordenação"),
    order_dir: str = Query(default="asc", regex="^(asc|desc)$", description="Direção da ordenação"),
    db: Session = Depends(get_session)
):
    pagination = PaginationParams(page=page, size=size)
    
    return UserService(db).get_paginated(
        pagination=pagination,
        order_by=order_by,
        order_dir=order_dir
    )

@router.get("/{id}", response_model=UserResponse, status_code=HTTPStatus.OK)
def get_by_id(id: str, db: Session = Depends(get_session)):
    return UserService(db).get_by_id(id)
