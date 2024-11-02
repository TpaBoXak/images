from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

from sqlalchemy import select


async def get_user_by_nickname(session: AsyncSession, nickname: str) -> User:
    stmt = select(User).where(User.nickname == nickname)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user

async def get_all_user(session: AsyncSession, user_id: int) -> dict:
    stmt = select(User.id, User.first_name, User.second_name,
            User.nickname).where(User.id != user_id)
    users_info: list[tuple] = await session.execute(stmt)
    
    result = {}
    for row in users_info:
        result[row[0]] = {
            "first_name": row[1],
            "second_name": row[2],
            "nickname": row[3]
        }

    return result

async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user

