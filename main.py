from typing import List, Annotated

from fastapi import FastAPI
from models.user import User, UserIN, Token
from databeses import database, users

from permissions import create_access_token, get_password_hash, authenticate_user, get_current_active_user, PermissionChecker
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, FastAPI, HTTPException, status

from pprint import pprint

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=User)
async def create_user(user: UserIN, permi : bool = Depends(PermissionChecker(required_permissions=["1"]))):
    query = users.insert().values(username=user.username, email=user.email,
                                  rights=user.rights, hashed_password=get_password_hash(user.password),
                                  disabled=user.disabled)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.get("/users/", response_model=List[User])
async def read_user(permi : bool = Depends(PermissionChecker(required_permissions=["1"]))):
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/me/", response_model=UserIN)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):  
    user = await authenticate_user(form_data.username, form_data.password)
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