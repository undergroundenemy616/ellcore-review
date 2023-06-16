from users.permissions import PermissionChecker
from databeses import database, db_goods, db_category, db_manager, db_organization, db_article
from goods.models import GoodsIn, GoodsUpdate
from users.models import User
from fastapi import HTTPException



async def create_good(good : GoodsIn, current_user: User):
  PermissionChecker(required_permissions=["goods.create"]
                    ).check_permission(current_user.permissions)
  await check_foreign_keys(dict(good))
  await check_unique(good)
  query = db_goods.insert().values(good.dict())
  last_record_id = await database.execute(query)
  return {**good.dict(), "id": last_record_id}

async def read_goods(current_user: User, all: bool):
  PermissionChecker(required_permissions=['goods.read']
                    ).check_permission(current_user.permissions)
  if (all):
    query = db_goods.select()
  else:
    query = db_goods.select().where(db_goods.c.archived == False)
  result = await database.fetch_all(query)
  # for i in result:
  #   print(dict(i))
  return result

async def patch_good(good: GoodsUpdate, current_user : User):
  PermissionChecker(required_permissions=["goods.create"]
                    ).check_permission(current_user.permissions)
  db = await database.fetch_one(db_goods.select().where(db_goods.c.id == good.id))
  if db == None:
    raise HTTPException(status_code=404, detail="Good not found to update")
  db = (dict(db))
  if db.get("article_wb") != good.article_wb:
      await check_unique(good)
  for k, v in good.dict().items():
      if v != None:
        db[k] = v
  print(db)
  await check_foreign_keys(db)
  query = db_goods.update().where(db_goods.c.id == db["id"]).values(db)
  await database.execute(query)
  return {**db}

async def check_unique(good : GoodsIn):
  query = db_goods.select().where(db_goods.c.article_wb == good.article_wb)
  res = await database.fetch_one(query)
  if res != None:
      raise HTTPException(status_code=404, detail="Good with that article already exists")
  return res

async def check_foreign_keys(good : dict) -> None:
  query = db_category.select().where(db_category.c.id == good['category_id'])
  res = await database.fetch_one(query)
  if res == None:
      raise HTTPException(status_code=404, detail="Category not found")
  
  query = db_manager.select().where(db_manager.c.id == good['manager_id'])
  res = await database.fetch_one(query)
  if res == None:
      raise HTTPException(status_code=404, detail="Manager not found")
  
  query = db_organization.select().where(db_organization.c.id == good['organization_id'])
  res = await database.fetch_one(query)
  if res == None:
      raise HTTPException(status_code=404, detail="Organization not found")
  
  query = db_article.select().where(db_article.c.id == good['article_id'])
  res = await database.fetch_one(query)
  if res == None:
      raise HTTPException(status_code=404, detail="Article not found")