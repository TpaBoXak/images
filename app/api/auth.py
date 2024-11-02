from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from datetime import timedelta 

from config import settings
from app import redis_client

from app import db_helper
from app.schemas.users import UserBaseSchema
from app.dao import users as user_dao
from app.jwt import jwt as jwt_confirm
from app.models import User


router: APIRouter = APIRouter(prefix=settings.api.auth_prefix)

@router.post("")
async def auth(user_schema: UserBaseSchema, 
    session: AsyncSession = Depends(db_helper.session_getter)
):
    user: User = await user_dao.get_user_by_nickname(session=session, 
            nickname=user_schema.nickname)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect nickname or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not await jwt_confirm.verify_password(user_schema.password,
            user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect nickname or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "user_id": user.id,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "nickname": user.nickname,
    }
    access_token_expires = timedelta(hours=settings.jwt.token_hours)
    access_token = jwt_confirm.create_access_token(data=token_data,
            expires_delta=access_token_expires)
    
    await redis_client.set(access_token, "True", ex=43200)
    
    return {"access_token": access_token, "token_type": "bearer"}