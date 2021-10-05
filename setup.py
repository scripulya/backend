from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm.session import sessionmaker

from credentials import DATABASE_CREDENTIALS

user = DATABASE_CREDENTIALS['user']
host = DATABASE_CREDENTIALS['host']
password = DATABASE_CREDENTIALS['password']
port = DATABASE_CREDENTIALS['port']
database = DATABASE_CREDENTIALS['database']

db_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
engine = create_async_engine(db_uri, echo=True, future=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
