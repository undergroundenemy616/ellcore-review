from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


"""Название класса с маленькой буквы"""
class hash:
  def __init__(self) -> None: # 2 отступа вместо 4
    self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

  def get_password_hash(self, password):
      return self.pwd_context.hash(password)

  def verify_password(self, plain_password, hashed_password):
      return self.pwd_context.verify(plain_password, hashed_password)