from fastapi import FastAPI
# дублирование импорта
from databeses import database
from fastapi import FastAPI
from users.views import user_router, token_router
from goods.views import goods_router
from organizations.views import organization_router
import uvicorn
# импорты расставлены не по pep
app = FastAPI()

@app.on_event("startup") # PEP8 E302
async def startup():
    await database.connect()

@app.on_event("shutdown") # PEP8 E302
async def shutdown():
    await database.disconnect()

app.include_router(user_router)
app.include_router(token_router)
app.include_router(organization_router)
app.include_router(goods_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # Порт лучше вынетси в енву.

# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     return await UserServices().login_for_access_token(form_data)


    





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