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


"""
Ваш класс UserServices включает в себя некоторые хорошие практики, включая инкапсуляцию бизнес-логики 
в отдельный сервисный слой. Однако заметно, что класс также занимается обработкой HTTP-исключений, 
что, как правило, лучше выполнять на уровне роутера. Вот несколько причин, почему это важно:

1. Принцип единой ответственности: Сервисный слой должен фокусироваться на выполнении бизнес-логики, 
в то время как обработка HTTP-запросов и ответов должна выполняться на уровне роутера. 
Это улучшает модульность и читаемость кода, а также облегчает его тестирование и отладку.

2. Повторное использование кода: Сервисные классы могут быть использованы в различных контекстах, 
не обязательно связанных с HTTP (например, в фоновых задачах, консольных командах и т. д.). 
Внедрение специфической для HTTP логики в сервисный слой ограничивает его повторное использование.


3. Тестирование: Разделение логики обработки HTTP и бизнес-логики упрощает тестирование обоих 
этих аспектов независимо друг от друга.
"""


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


  """
  Функция check_unique в текущем виде несет в себе избыточную функциональность. 
  Если цель состоит в том, чтобы проверить, существует ли пользователь с определенным email 
  в базе данных, то гораздо более эффективным подходом было бы использование уже существующего 
  метода для получения пользователя по ID. Вместо того, чтобы вызывать отдельный метод check_unique, 
  который по сути выполняет похожую операцию, можно просто вызвать метод read_user_by_id и проверить, 
  вернул ли он пользователя или None. Это обеспечит более ясное разделение ответственности и э
  ффективное использование кода.
  """
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
    """Можно проще -> if not res:"""
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return res


  async def update_user(self, id, user: User, current_user : User):
    PermissionChecker(required_permissions=[]).check_permission(current_user.permissions)
    """Что за коммент?"""
    # print(user.permissions)
    validate_permissions(user.permissions)
    """
    Обратите внимание на нейминг переменной db в данной строке кода. 
    Такой выбор имени переменной может привести к путанице, поскольку обычно db используется для
     обозначения экземпляра базы данных или подключения к ней, а не для хранения результатов запроса. 
     В данном случае более подходящим названием для переменной, хранящей данные пользователя, может быть,
      например, user.

    Важно, чтобы имена переменных отражали их назначение и содержимое. Правильный выбор имен 
    переменных может сделать код более понятным и читаемым, что облегчит поддержку и развитие кода в
     долгосрочной перспективе.

    В этом контексте рекомендуется ознакомиться с книгой Роберта Мартина "Чистый код: создание,
     анализ и рефакторинг". Это обязательное чтение для каждого программиста, независимо от его
     уровня опыта. Эта книга предлагает ценные советы и примеры, которые помогут вам улучшить свои
      навыки программирования. Она обучает писать код, который не только работает, но и является чистым,
       легко поддерживаемым и развиваемым. В частности, одна из глав посвящена правильному выбору имен 
       переменных и функций, что особенно актуально в данном контексте.
    """
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