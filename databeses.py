from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
import databases
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DATE, TEXT
from sqlalchemy import String, Boolean, VARCHAR, NUMERIC, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from users.hash import hash

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

database = databases.Database(DATABASE_URL)

metadata = MetaData()

db_users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False, default=None, unique=True),
    Column("hashed_password", String, default=None),
    Column("disabled", Boolean, default=False),
    Column("archived", Boolean, default=False),
    Column("permissions", JSONB),
)

db_organization = Table(
    "organization",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("name", VARCHAR(255), nullable=False),
    Column("inn", VARCHAR(255), nullable=False, unique=True),
    Column("standard_token", String, default=None),
    Column("statistics_token", String, default=None),
    Column("advertizing_token", String, default=None),
    Column("archived", Boolean, default=False),
)

db_manager = Table(
    "manager",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("first_name", VARCHAR(255), nullable=False),
    Column("last_name", VARCHAR(255), nullable=False),
    Column("patronymic", VARCHAR(255), default=None),
    Column("archived", Boolean, default=False),
)

db_category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("name", VARCHAR(255), nullable=False, unique=True),
)

db_goods = Table(
    "goods",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("article_wb", VARCHAR(255), nullable=False, unique = True),
    Column("manager_id", Integer, ForeignKey("manager.id")),
    Column("zero_cost", NUMERIC),
    Column("average_price", NUMERIC),
    Column("optimal_price", NUMERIC),
    Column("article_code", VARCHAR(255), nullable=False),
    Column("article_options", VARCHAR(255), nullable=False),
    Column("organization_id", Integer, ForeignKey("organization.id")),
    Column("category_id", Integer, ForeignKey("category.id"), nullable=False),
    Column("archived", Boolean, default=False)
)

db_netcost = Table(
    "netcost",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("goods_id", Integer, ForeignKey("goods.id"), nullable=False),
    Column("value", NUMERIC, nullable=False),
)

db_goods_size = Table(
    "goods_size",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("goods_id", Integer, ForeignKey("goods.id"), nullable=False),
    Column("size", VARCHAR(255), nullable=False),
    Column("barcode", VARCHAR(255), nullable=False, unique=True),
    UniqueConstraint("goods_id", "size")
)

db_goods_wb = Table(
    "goods_wb",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("goods_id", Integer, ForeignKey("goods.id"), nullable=False),
    Column("organization_id", Integer, ForeignKey("organization.id"), nullable=False),
    Column("article_wb", VARCHAR(255), nullable=False, unique=True),
)

db_self_buyout = Table(
    "self_buyout",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("data", DATE),
    Column("goods_size_id", Integer, ForeignKey("goods_size.id"), nullable=False),
    Column("planned_quantity", Integer),
    Column("planned_price", NUMERIC),
    Column("actual_quantity", Integer),
    Column("actual_price", NUMERIC),
    Column("actual_cost", NUMERIC),
)

db_advertising_type = Table(
    "advertising_type",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("name", VARCHAR(255), nullable=False, unique=True),
)

db_advertising = Table(
    "advertising",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("date", DATE),
    Column("goods_size_id", Integer, ForeignKey("goods_size.id"), nullable=False),
    Column("type_id", Integer, ForeignKey("advertising_type.id"), nullable=False),
    Column("cost", NUMERIC),
    Column("comment", TEXT),
    Column("views", Integer),
    Column("frequency", Integer),
    Column("clicks", Integer),
    Column("ctr", NUMERIC),
    Column("cpc", NUMERIC),
    Column("add_to_cart", Integer),
    Column("orders", Integer),
    Column("amount", NUMERIC),
)

db_goods_report = Table(
    "goods_report",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("goods_wb_id", Integer, ForeignKey("goods_wb.id"), nullable=False),
    Column("date", DATE),
    Column("orders_rate_7", NUMERIC),
    Column("sales_rate_7", NUMERIC),
    Column("free_wb", Integer),
    Column("on_way_wb", Integer),
    Column("in_stock_1c", Integer),
    Column("in_tailoring", Integer),
    Column("in_stock_ff", Integer),
    Column("on_way_ff", Integer),
    Column("in_production", Integer),
)

metadata.create_all(engine)
# создание суперпользователя
s = db_users.select().where(db_users.c.email == "2")
conn = engine.connect()
result = conn.execute(s).fetchall()
if not len(result):
    ins = db_users.insert().values(username="2", hashed_password=hash.get_password_hash(hash(), "2"),
                                disabled=False, permissions = [1], email="2")
    print(ins)
    conn = engine.connect()
    result = conn.execute(ins)
# создание тестовых данных (все что ниже - удалить)
s = db_category.select().where(db_category.c.name == "Платья")
conn = engine.connect()
result = conn.execute(s).fetchall()
if not len(result):
    ins = db_category.insert().values(name="Платья")
    conn = engine.connect()
    result = conn.execute(ins)

s = db_manager.select().where(db_manager.c.first_name == "Иван",
                              db_manager.c.last_name == "Иванов",
                              db_manager.c.patronymic == "Иванович")
conn = engine.connect()
result = conn.execute(s).fetchall()
if not len(result):
    ins = db_manager.insert().values(first_name="Иван", last_name="Иванов", patronymic="Иванович")
    conn = engine.connect()
    result = conn.execute(ins)

s = db_organization.select().where(db_organization.c.inn == "123")
conn = engine.connect()
result = conn.execute(s).fetchall()
if not len(result):
    ins = db_organization.insert().values(name="elcora", inn="123",
                                          standard_token = "standart_token",
                                          statistics_token = "statistic_token",
                                          advertizing_token = "advertizing_token",
                                          archived = False)
    conn = engine.connect()
    result = conn.execute(ins)