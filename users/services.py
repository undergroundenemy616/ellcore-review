from fastapi import HTTPException, status, Depends
from users.models import User, UserIn, TokenData
from databeses import database, db_users
from users.permissions import PermissionChecker, validate_permissions
from users.hash import hash
from fastapi.security import OAuth2PasswordRequestForm
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from datetime import timedelta, datetime
from typing import Union, Annotated
from jose import JWTError, jwt
import json

class UserServices:
  async def create_user(self, user: UserIn, current_user : User):
    PermissionChecker(required_permissions=[]).check_permission(current_user.permissions)
    validate_permissions(user.permissions)
    await self.check_unique(user)
    query = db_users.insert().values(username=user.username,
                                  email=user.email,
                                  disabled=user.disabled,
                                  archived=user.archived,
                                  permissions=user.permissions,
                                  hashed_password=hash().get_password_hash(user.password))
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}
  
  async def check_unique(self, current_user : UserIn):
    query = db_users.select().where(db_users.c.email == current_user.email)
    res = await database.fetch_all(query)
    if len(res):
        raise HTTPException(status_code=400, detail="User with that email already exists")
    return res
  
  async def read_user_by_id(self, id: int, current_user : User):
    PermissionChecker(required_permissions=[]).check_permission(current_user.permissions)
    query = db_users.select().where(db_users.c.id == id)
    res = await database.fetch_one(query)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return res

  async def update_user(self, id, user: User, current_user : User):
    PermissionChecker(required_permissions=[]).check_permission(current_user.permissions)
    # print(user.permissions)
    validate_permissions(user.permissions)
    db = await database.fetch_one(db_users.select().where(db_users.c.id == id))

    if db == None:
      raise HTTPException(status_code=404, detail="User not found to update")
    db = (dict(db))
    if db.get("email") != user.email:
      await self.check_unique(user)

    for k, v in user.dict().items():
       if v != None:
          if k == "password":
             k = "hashed_password"
          db[k] = v
    query = db_users.update().where(db_users.c.id == db["id"]).values(db)
    await database.execute(query)
    return {**db}

  async def login_for_access_token(self,
    form_data : OAuth2PasswordRequestForm):  
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
  
  async def read_user(self, current_user: User, all: bool,
                      skip, limit):
    PermissionChecker(required_permissions=[]).check_permission(current_user.permissions)
    if (all):
      query = db_users.select().limit(limit).offset(skip)
    else:
      query = db_users.select().where(db_users.c.archived == False).limit(limit).offset(skip)
    return await database.fetch_all(query)

  def normalize(self, user : UserIn):
    for i in dict(user):
        if dict(user)[i] == None:
            dict(user)[i] = False if i != 'permissions' else []

 
async def get_current_user(token: Annotated[str, Depends(hash().oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_user(email: str):
    query = "SELECT * FROM users WHERE email = :email"
    result = await database.fetch_one(query=query, values={"email": email})
    if result == None:
       raise HTTPException(status_code=404, detail="Wrong email or password")
    temp = dict(result)
    
    if email in result["email"]:
        temp["permissions"]=json.loads(temp["permissions"])
        return User(**temp)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not hash().verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt