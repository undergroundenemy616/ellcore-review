from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
import databases
import sqlalchemy

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

rules = ["null", "read", "write", "admin"]

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("rights", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("disabled", sqlalchemy.Boolean, default=False),
)


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
