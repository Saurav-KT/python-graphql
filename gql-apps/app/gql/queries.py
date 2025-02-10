from graphene import ObjectType, List, Field, Int
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject
from app.db.database import async_session_maker
from app.db.models import Job, Employer, User, JobApplication
from sqlmodel import select
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, job_id=Int(required=True))
    employer = Field(EmployerObject, employer_id=Int(required=True))
    employers = List(EmployerObject)
    users = List(UserObject)
    job_applications = List(JobApplicationObject)

    @staticmethod
    async def resolve_job_applications(root, info):
        async with async_session_maker() as session:
            job_application = (await session.exec(select(JobApplication).options(joinedload(JobApplication.job)).options(joinedload(JobApplication.user)))).all()
            return job_application

    @staticmethod
    async def resolve_users(root, info):
        async with async_session_maker() as session:
            user = (await session.exec(select(User))).all()
            return user

    @staticmethod
    async def resolve_employer(root, info, employer_id):
        async with async_session_maker() as session:
            employer = (await session.exec(
                select(Employer).options(joinedload(Employer.jobs)).where(Employer.id == employer_id))).first()
            # employer = (await session.exec(select(Employer).where(Employer.id == employer_id))).first()
            return employer

    @staticmethod
    async def resolve_job(root, info, job_id):
        async with async_session_maker() as session:
            job = (await session.exec(select(Job).options(joinedload(Job.employer)).options(joinedload(Job.applications).lazyload(JobApplication.user)).where(Job.id == job_id))).first()
            return job

    @staticmethod
    async def resolve_jobs(root, info):
        # return jobs_data
        async with async_session_maker() as session:
            query = select(Job).options(joinedload(Job.employer))
            x = await session.exec(query)
            return x.all()

    @staticmethod
    async def resolve_employers(root, info):
        # return employers_data
        async with async_session_maker() as session:
            # query = select(Employer).options(joinedload(Employer.jobs))
            # query = select(Employer)
            employers = (await session.exec(select(Employer).options(joinedload(Employer.jobs)))).unique().all()
            return employers
