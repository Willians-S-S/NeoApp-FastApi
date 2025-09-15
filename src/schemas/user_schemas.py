from datetime import date, datetime

from fastapi import HTTPException
from http import HTTPStatus
from pydantic import BaseModel, EmailStr, Field, field_validator
from validate_docbr import CPF

class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    birthday: date = Field(lt=date.today())
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=100)
    phone: str = Field()
    cpf: str = Field(min_length=11, max_length=11)

    @field_validator("cpf")
    def validate_cpf(cls, cpf: str):
    
        if not CPF().validate(cpf):
            raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, "CPF inválado.")
        
        return cpf


class UserResponse(BaseModel):
    id: str
    name: str
    age: int
    email: EmailStr
    password: str
    phone: str
    cpf: str
    creat_at: datetime
    update_at: datetime