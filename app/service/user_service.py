from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import schemas
from models import User
from utils.auth_util import pwd_context, verify_password, create_access_token
from dao import user_dao, shelf_dao 

# 创建用户
async def create_user(db: Session, user: schemas.UserCreate):
    # 检查用户名是否唯一
    existing_user = await user_dao.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    user.password = pwd_context.hash(user.password)
    db_user = await user_dao.create_user(db, user)
    return db_user

# 用户登录
async def authenticate_user(db: Session, user: schemas.UserLogin):
    password = user.password
    user = await user_dao.get_user_by_username(db, user.username)
    # 用户不存在
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # 密码错误
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    # 更新用户登录状态
    user = await user_dao.update_user_login_status(db, user, True)
    # 生成并返回 JWT 令牌
    access_token = create_access_token(data={"sub": user.username})
    return access_token

# 用户登出
async def logout_user(db: Session, user: User):
    user = await user_dao.update_user_login_status(db, user, False)
    return user

# 获取用户书架
async def get_user_shelf(db: Session, user: User):
    user_id = user.id
    shelfs = await shelf_dao.get_user_shelf(db, user_id)
    shelfs = [schemas.ShelfInDB.model_validate(shelf, from_attributes=True) for shelf in shelfs]
    return shelfs
