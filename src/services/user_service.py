from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

from core.errors import conflict, not_found
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

        return self.__to_response(user_save)
    
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
            self.__to_response(user) 
            for user in users
        ]
        
        return PageResponse.create(
            items=user_responses,
            total=total,
            page=pagination.page,
            size=pagination.size
        )
    
    def __to_response(self, user: UserModel) -> UserResponse:
        age = relativedelta(date.today(), user.birthday).years

        return UserResponse(
            id=user.id,
            name=user.name,
            age=age,
            email=user.email,
            password=user.password,
            phone=user.phone,
            cpf=user.cpf,
            creat_at=user.creat_at,
            update_at=user.update_at
            )
