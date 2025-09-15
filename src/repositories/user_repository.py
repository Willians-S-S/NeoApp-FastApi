from datetime import date
from fastapi import HTTPException
from http import HTTPStatus

from typing import Optional, List
from sqlalchemy import asc, desc, select, and_
from sqlalchemy.orm import Session

from db.models.user_models import UserModel
from core.errors import conflict

class UserRepository:

    def __init__(self, session: Session):
        self.__session = session

    def save(self, user: UserModel) -> UserModel:
        try:
            user_save = self.__session.merge(user)
            self.__session.commit()
            return user_save
        except Exception as e:
            self.__session.rollback()
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))

    def get_by_id(self, id: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.id == id)
        result = self.__session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_email(self, email: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.email == email)
        result = self.__session.execute(stmt)
        return result.scalar_one_or_none()
    
    def get_by_cpf(self, cpf: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.cpf == cpf)
        result = self.__session.execute(stmt)
        return result.scalar_one_or_none()
    
    def get_paginated(
        self, 
        offset: int, 
        limit: int, 
        order_by: Optional[str] = None,
        order_dir: str = "asc"
    ) -> tuple[List[UserModel], int]:
    
        query = self.__session.query(UserModel)
        
        total = query.count()

        if order_by is not None:
            if hasattr(UserModel, order_by):
                column = getattr(UserModel, order_by)
                if order_dir.lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))
        
        users = query.offset(offset).limit(limit).all()
        
        return users, total

    def get_user_with_attributes(
            self,
            name: Optional[str] = None,
            email: Optional[str] = None,
            cpf: Optional[str] = None,
            phone: Optional[str] = None,
            birthday: Optional[date] = None,
    ) -> UserModel:
        
        conditions = []
        if name:
            conditions.append(UserModel.name == name)
        if email:
            conditions.append(UserModel.email == email)
        if cpf:
            conditions.append(UserModel.cpf == cpf)
        if phone:
            conditions.append(UserModel.phone == phone)
        if birthday:
            conditions.append(UserModel.birthday == birthday)

        stmt = select(UserModel).where(and_(*conditions)).limit(1)

        return self.__session.execute(stmt).scalar_one_or_none()
        
    def delete(self, user: UserModel) -> None:
        try:
            self.__session.delete(user)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))