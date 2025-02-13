from sqlmodel import SQLModel
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Employer, Job, User, JobApplication
from app.settings.config import DATABASE_URL
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.data import employers_data, jobs_data, users_data, application_data
from app.utils import hash_password

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_schema():
    async with engine.begin() as connection:
        await connection.run_sync(lambda conn: conn.execute(CreateSchema("gql_test", if_not_exists=True)))


async def init_db():
    await create_schema()
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        for employer in employers_data:
            session.add(Employer(**employer))

        for job in jobs_data:
            session.add(Job(**job))

        for user in users_data:
            user['password_hash']= hash_password(user['password'])
            del user['password']
            session.add(User(**user))

        for app in application_data:
            session.add(JobApplication(**app))
        await session.commit()
