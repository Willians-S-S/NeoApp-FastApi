from fastapi import HTTPException
from http import HTTPStatus

from sqlalchemy import select
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
    
    def delete(self, user: UserModel) -> None:
        try:
            self.__session.delete(user)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))