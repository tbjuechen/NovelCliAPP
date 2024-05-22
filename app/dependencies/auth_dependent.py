from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Union
import jwt

from dependencies.db_dependent import get_db
from utils.auth_util import decode_access_token, decode_access_token_without_verification
from dao import user_dao
from models import User

# 依赖项，用于从请求中获取令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") 
    # token 过期
    except jwt.ExpiredSignatureError:
        username = decode_access_token_without_verification(token).get("sub")
        user = await user_dao.get_user_by_username(db, username)
        await user_dao.update_user_login_status(db, user, False) # 更新用户登录状态
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    # token 无效
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user: Union[User, None] = await user_dao.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.is_logged_in == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not logged in")
    return user