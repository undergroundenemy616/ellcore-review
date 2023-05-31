from typing import List, Union, Annotated

from fastapi import FastAPI
from schemas import User, UserIN
from databeses import database, users, rules
from schemas import Token, TokenData

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status

from pprint import pprint

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = await get_user(users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_user(db, username: str):
    query = "SELECT * FROM users WHERE username = :username"
    result = await database.fetch_one(query=query, values={"username": username})
    if username in result["username"]:
        user_dict = result
        return UserIN(**user_dict, password=user_dict["hashed_password"])

app = FastAPI()

def get_password_hash(password):
    return pwd_context.hash(password)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=User)
async def create_note(note: UserIN):
    query = users.insert().values(username=note.username, email=note.email,
                                  rights=note.rights, hashed_password=get_password_hash(note.password),
                                  disabled=note.disabled)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

@app.get("/users/", response_model=List[User])
async def read_notes():
    query = users.select()
    return await database.fetch_all(query)

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me/", response_model=UserIN)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):  
    user = await authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



async def authenticate_user(fake_db, username: str, password: str):
    user = await get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user




# @app.post("/add_user", response_model=Token)
# async def add_user(
#     current_user: Annotated[User, Depends(get_current_active_user)],
#     form_data: Annotated[User_to_add, Depends()]
# ):  
#     hashed_password = get_password_hash(form_data.password)
#     username = form_data.username
#     email = form_data.email
#     full_name = form_data.full_name
#     fake_users_db[username] = {
#         "username": username,
#         "hashed_password": hashed_password,
#         "email": email,
#         "full_name": full_name,
#         "disabled": False,
#         "rights": []
#     }
#     print(fake_users_db[username])
#     return {"access_token": current_user.username, "token_type": "bearer"}

# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

# @app.get("/data/{path:path}")
# async def get_data(path:str,
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": path, "owner": current_user.username}]


# @app.get("/data/{path:path}")
# async def get_data(path:str,
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": path, "owner": current_user.username}]