from users.permissions import PermissionChecker
from databeses import database, db_organization
from organizations.models import OrganizationIn, OrganizationOut, OrganizationUpdate
from users.models import User
from fastapi import HTTPException, status, Depends
from pprint import pprint

class OrganizationServices:
  async def create_organization(self, organization: OrganizationIn, current_user: User):
    PermissionChecker(required_permissions=[]).check(current_user.permissions)
    # OrganizationServices().normalize(organization)
    print(organization.archived)
    await OrganizationServices().check_unique(organization)
    query = db_organization.insert().values(name=organization.name,
                                            inn=organization.inn,
                                            # standard_token=organization.standard_token,
                                            # statistics_token=organization.statistics_token,
                                            # advertizing_token=organization.advertizing_token,
                                            archived=organization.archived)
    last_record_id = await database.execute(query)
    return {**organization.dict(), "id": last_record_id}
  
  # async def archive_user_by_id(self, id: int, current_user : User):
  #   PermissionChecker(required_permissions=[]).check(current_user.permissions)
  #   query = users.update().where(users.c.id == id).values(archived=True)
  #   res = await database.fetch_all(query)
  #   if len(res) == 0:
  #       raise HTTPException(status_code=404, detail="User not found")
  #   return res
  
  async def get_organization_by_id(self, id: int, current_user : User):
    PermissionChecker(required_permissions=[]).check(current_user.permissions)
    query = db_organization.select().where(db_organization.c.id == id)
    res = await database.fetch_all(query)
    if len(res) == 0:
        raise HTTPException(status_code=404, detail="Organization not found")
    return res

  async def read_organization(self, current_user: User, all: bool):
    PermissionChecker(required_permissions=[]).check(current_user.permissions)
    if (all):
      query = db_organization.select()
    else:
      query = db_organization.select().where(db_organization.c.archived == False)
    return await database.fetch_all(query)

  async def update_organization(self, organization: OrganizationUpdate, current_user : User):
    PermissionChecker(required_permissions=[]).check(current_user.permissions)
    # await OrganizationServices().normalize(organization)
    # await OrganizationServices().check_unique(organization)
    d = await OrganizationServices().get_organization_by_id(id=organization.id,
                                                            current_user=current_user)
    for i in dict(organization):
      if dict(organization)[i] == None:
        dict(organization)[i] = d[0][i]
        pprint(dict(organization)[i])
        pprint(d[0][i])
    
    query = db_organization.update().where(db_organization.c.id == d[0]["id"],
                                           db_organization.c.inn == d[0]["inn"]).values(
                                                  id=organization.id,
                                                  name=organization.name,
                                                  inn=organization.inn,
                                                  # standard_token=organization.standard_token,
                                                  # statistics_token=organization.statistics_token,
                                                  # advertizing_token=organization.advertizing_token,
                                                  archived=organization.archived)
    await database.execute(query)
    return {**organization.dict()}

  async def update_organization1(self, organization: OrganizationUpdate, current_user : User):
    print(2)
    PermissionChecker(required_permissions=[]).check(current_user.permissions)
    db_org = await OrganizationServices().get_organization_by_id(id=organization.id,
                                                            current_user=current_user).one_or_none()
    if db_org is not None:
      print(db_org)
      update_data = organization.dict(exclude_unset=True)
    # for i organization:
    #   if dict(organization)[i] == None:
    #     dict(organization)[i] = d[0][i]
    #     pprint(dict(organization)[i])
    #     pprint(d[0][i])
      query = db_organization.update(update_data).where(db_organization.c.id == d[0]["id"])
      await database.execute(query)
    else: 
      raise HTTPException(status_code=404, detail="else")
    # query = db_organization.update().where(db_organization.c.id == d[0]["id"],
    #                                        db_organization.c.inn == d[0]["inn"]).values(
    #                                               id=organization.id,
    #                                               name=organization.name,
    #                                               inn=organization.inn,
    #                                               # standard_token=organization.standard_token,
    #                                               # statistics_token=organization.statistics_token,
    #                                               # advertizing_token=organization.advertizing_token,
    #                                               archived=organization.archived)
    # await database.execute(query)
    return {**organization.dict()}

  async def check_unique(self, organization: OrganizationIn):
    # pprint(organization.inn)
    # pprint(db_organization.c['inn'])
    # if (db_organization.c.inn == organization.inn):
    #   return 1
    query = db_organization.select().where(db_organization.c.inn == organization.inn)
    res = await database.fetch_all(query)
    if len(res):
        raise HTTPException(status_code=400, detail="Organization with that inn already exists")
    return 1
  
  def normalize(self, organization : OrganizationUpdate):
    for i in dict(organization):
      # print(i)
      # print(1)
      print(db_organization.c)
      # if dict(organization)[i] == None:
      #     dict(organization)[i] = db_organization.
 