from users.permissions import PermissionChecker
from databeses import database, db_organization
from organizations.models import OrganizationIn, OrganizationOut, OrganizationUpdate
from users.models import User
from fastapi import HTTPException, status, Depends
from pprint import pprint

async def create_organization(organization: OrganizationIn, current_user: User):
  PermissionChecker(required_permissions=[6]).check_permission(current_user.permissions)
  await check_unique(organization)
  query = db_organization.insert().values(organization.dict())
  last_record_id = await database.execute(query)
  return {**organization.dict(), "id": last_record_id}

async def archive_organization(id : int, current_user : User):
  PermissionChecker(required_permissions=[7]
                    ).check_permission(current_user.permissions)
  db = await database.fetch_one(db_organization.select().where(db_organization.c.id == id))
  if db == None:
    raise HTTPException(status_code=404, detail="Organization not found to archive")
  db = (dict(db))
  db["archived"] = True
  query = db_organization.update().where(db_organization.c.id == id).values(db)
  await database.execute(query)
  return {**db}

async def get_organization_by_id(id: int, current_user : User):
  PermissionChecker(required_permissions=[5]).check_permission(current_user.permissions)
  query = db_organization.select().where(db_organization.c.id == id)
  res = await database.fetch_one(query)
  if len(res) == 0:
      raise HTTPException(status_code=404, detail="Organization not found")
  return res

async def read_organization(current_user: User, all: bool, skip, limit):
  PermissionChecker(required_permissions=[5]).check_permission(current_user.permissions)
  if (all):
    query = db_organization.select().limit(limit).offset(skip)
  else:
    query = db_organization.select().where(db_organization.c.archived == False).limit(limit).offset(skip)
  return await database.fetch_all(query)

async def update_organization(id, organization: OrganizationUpdate, current_user : User):
  PermissionChecker(required_permissions=[]).check_permission(current_user.permissions)
  db = await database.fetch_one(db_organization.select().where(db_organization.c.id == id))
  if db == None:
    raise HTTPException(status_code=404, detail="Organization not found to update")
  db = (dict(db))
  if db.get("inn") != organization.inn:
      await check_unique(organization)
  for k, v in organization.dict().items():
      if v != None:
        db[k] = v
  query = db_organization.update().where(db_organization.c.id == db["id"]).values(db)
  await database.execute(query)
  return {**db}

async def check_unique(organization : OrganizationIn):
  query = db_organization.select().where(db_organization.c.inn == organization.inn)
  res = await database.fetch_one(query)
  if res != None:
      raise HTTPException(status_code=404, detail="Organization with that inn already exists")
  return res
 