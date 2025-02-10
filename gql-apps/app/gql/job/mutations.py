from graphene import Mutation, String, Int, Field, Boolean
from app.gql.types import JobObject
from app.db.database import async_session_maker
from app.db.models import Job
from sqlmodel import select
from sqlalchemy.orm import joinedload


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    async def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        async with async_session_maker() as session:
            session.add(job)
            await session.commit()
            await session.refresh(job)
            return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    async def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        async with async_session_maker() as session:
            # query = select(Job).where(Job.id == job_id)
            # results = await session.exec(query)
            # job = results.first()
            query = await session.exec(select(Job).options(joinedload(Job.employer)).where(Job.id == job_id))
            job = query.first()
            if not job:
                raise Exception("job not found")
            if title is not None:
                job.title = title

            if description is not None:
                job.description = description

            if employer_id is not None:
                job.employer_id = employer_id

            await session.commit()
            await session.refresh(job)
            return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        job_id = Int(required=True)

    success = Boolean()
    message = String()

    @staticmethod
    async def mutate(root, info, job_id):
        async with async_session_maker() as session:
            job = (await session.exec(select(Job).where(Job.id == job_id))).first()
            if not job:
                return DeleteJob(success=False, message="Job not found")
            await session.delete(job)
            await session.commit()
            return DeleteJob(success=True, message="Job deleted successfully")

