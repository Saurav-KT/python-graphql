from sqlmodel import create_engine
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from loguru import logger
from sqlmodel import Column, DateTime, Enum, Field, MetaData, SQLModel, Relationship
from uuid import UUID, uuid4
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from sqlalchemy.schema import CreateSchema
import asyncio


# metadata = MetaData(schema="gql_test")
# SQLModel.metadata = metadata


class BaseModel(SQLModel):
    metadata = MetaData(schema="gql_test")
    SQLModel.metadata = metadata


# class BaseModel(SQLModel):
#     class Config:
#         metadata = metadata


class Employer(BaseModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, title="employer name")
    contact_email: str | None = Field(default=None, title="employer contact email ", max_length=200)
    industry: str = Field(nullable=False, title="employer industry")
    job: "Job" = Relationship(back_populates="employer")


class Job(BaseModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(nullable=False, title="job title")
    description: str = Field(nullable=False, title="job description")
    employer_id: int = Field(title="employer table foreign key field", foreign_key="employer.id")
    employer: Employer | None = Relationship(back_populates="job")


load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# ensure schema exists
async def create_schema():
    async with engine.begin() as connection:
        await connection.run_sync(lambda conn: conn.execute(CreateSchema("gql_test", if_not_exists=True)))


async def init_db():
    await create_schema()
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def main():
    # Initialize the database and create tables
    await init_db()

    employers_data = [{"id": 1, "name": "Cisco", "contact_email": "test@cisco.com", "industry": "tech"},
                      {"id": 2, "name": "Zee", "contact_email": "test@zee.com", "industry": "Entertainment"},
                      ]
    jobs_data = [
        {"id": 1, "title": "software engineer", "description": "develop web & mobile application", "employer_id": 1},
        {"id": 2, "title": "Marketing expert", "description": "Generates sales lead and prepare a report",
         "employer_id": 1},
        {"id": 3, "title": "Accountant II", "description": "Manage financial records", "employer_id": 2}
    ]




    # Use the session for any database operations
    # async with async_session_maker() as session:
    #     employer = Employer(name="John Doe", contact_email="john.doe@example.com", industry="Finance")
    #     session.add(employer)
    #     await session.commit()
    async with async_session_maker() as session:
        for employer in employers_data:
            session.add(Employer(**employer))

        for job in jobs_data:
            session.add(Job(**job))
        await session.commit()



if __name__ == "__main__":
    asyncio.run(main())
