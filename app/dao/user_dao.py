from sqlalchemy.orm import Session
from datetime import datetime
from typing import Union

from models import User
from schemas import UserCreate


# 根据id获取用户
async def get_uset_by_id(db: Session, user_id: int) -> Union[User, None]:
    return db.query(User).filter(User.id == user_id).first()

# 根据用户名获取用户
async def get_user_by_username(db: Session, username: str) -> Union[User, None]:
    return db.query(User).filter(User.username == username).first()

# 创建用户
async def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 更新用户登录状态
async def update_user_login_status(db: Session, user: User, status: bool) -> User:
    user.is_logged_in = status
    db.commit()
    db.refresh(user)
    return user

# 更新用户最后登录时间
async def update_user_last_login(db: Session, user: User) -> User:
    user.last_login = datetime.now()
    db.commit()
    db.refresh(user)
    return user