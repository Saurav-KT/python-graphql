from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import init_db, async_session_maker
from app.gql.queries import Query
from app.gql.mutations import Mutation
from app.db.models import Employer, Job
from sqlmodel import select
from contextlib import asynccontextmanager

schema = Schema(query=Query, mutation=Mutation)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def startup_event():
#     await init_db()


@app.get("/employers")
async def get_employers():
    async with async_session_maker() as session:
        employers = await session.exec(select(Employer))
        await session.close()
        return employers.all()


@app.get("/jobs")
async def get_jobs():
    async with async_session_maker() as session:
        white_collor_job = await session.exec(select(Job))
        await session.close()
        return white_collor_job.all()


app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))
