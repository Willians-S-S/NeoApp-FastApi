from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlalchemy.orm import Session

from db.db import get_session
from schemas.user_schemas import UserCreate, UserRespose
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRespose, status_code= HTTPStatus.CREATED)
def creat_user(user: UserCreate, db: Session = Depends(get_session)):
    return UserService(db).save(user=user)
 
