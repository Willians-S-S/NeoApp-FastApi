from datetime import datetime, timezone
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

from core.errors import conflict
from db.models.user_models import UserModel
from schemas.user_schemas import UserCreate, UserResponse
from schemas.page_schemas import PageResponse, PaginationParams
from repositories.user_repository import UserRepository 

class UserService:

    def __init__(self, session: Session):
        self.__repository = UserRepository(session=session)

    def save(self, user: UserCreate) -> UserResponse:
        user_on_bd = self.__repository.get_by_email(user.email)

        if user_on_bd is not None:
            raise HTTPException(HTTPStatus.CONFLICT, conflict.EMAIL_ALREADY_IN_USE)
        
        user_on_bd = self.__repository.get_by_cpf(user.cpf)

        if user_on_bd is not None:
            raise HTTPException(HTTPStatus.CONFLICT, conflict.CPF_ALREADY_IN_USE)
        
        now = datetime.now(timezone.utc)
        user_save = UserModel(
            id=str(uuid4()), 
            **user.model_dump(), 
            creat_at=now,
            update_at=now)
        
        user_save = self.__repository.save(user_save)

        return UserResponse.model_validate(user_save, from_attributes=True)
    
    def get_paginated(
        self, 
        pagination: PaginationParams,
        order_by: Optional[str] = None,
        order_dir: str = "asc"
    ) -> PageResponse[UserResponse]:
        
        users, total = self.__repository.get_paginated(
            offset=pagination.offset,
            limit=pagination.size,
            order_by=order_by,
            order_dir=order_dir
        )
        
        user_responses = [
            UserResponse.model_validate(user, from_attributes=True) 
            for user in users
        ]
        
        return PageResponse.create(
            items=user_responses,
            total=total,
            page=pagination.page,
            size=pagination.size
        )

