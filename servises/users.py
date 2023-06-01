from typing import List, Union, Annotated

from fastapi import FastAPI
from models.user import User, UserIN, Token, TokenData
from databeses import database, users, rules

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status

from pprint import pprint

class SeviceUser:
    def __init__(self) -> None:
      self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

      self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def get_current_user(self, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_user(self, username: str):
        query = "SELECT * FROM users WHERE username = :username"
        result = await database.fetch_one(query=query, values={"username": username})
        if username in result["username"]:
            user_dict = result
            return UserIN(**user_dict, password=user_dict["hashed_password"])
        
    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user