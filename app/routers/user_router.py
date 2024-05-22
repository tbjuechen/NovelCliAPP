from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

from schemas import UserLogin, AccessToken, UserInDB, UserCreate, ShelfReadInfo, ShelfInDB
from dependencies.db_dependent import get_db
from service import user_service
from dependencies.auth_dependent import get_current_user
from models import User

user_router = APIRouter(prefix="/user")

@user_router.post("/login", response_model= AccessToken, tags=["user"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user : UserLogin = UserLogin(username=form_data.username, password=form_data.password)
    access_token = await user_service.authenticate_user(db, user)
    return AccessToken(access_token=access_token, token_type="bearer")

@user_router.post("/register", response_model=UserInDB, tags=["user"])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await user_service.create_user(db, user)

@user_router.post("/logout", response_model=UserInDB, tags=["user"])
async def logout(user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)):
    return await user_service.logout_user(db, user)

@user_router.get("/shelf", response_model=List[ShelfInDB], tags=["user"])
async def get_shelf(user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)):
    return await user_service.get_user_shelf(db, user)

@user_router.get("/info", response_model= UserInDB, tags=["user"])
async def get_user_info(user: User = Depends(get_current_user)):
    return user