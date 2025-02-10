from graphene import Mutation, String, Int, Field, Boolean
from app.gql.types import EmployerObject
from app.db.database import async_session_maker
from app.db.models import Employer
from sqlmodel import select
from sqlalchemy.orm import joinedload


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    async def mutate(root, info, name, contact_email, industry):
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        async with async_session_maker() as session:
            session.add(employer)
            await session.commit()
            await session.refresh(employer)
            return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)
    message = String()

    async def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):
        async with async_session_maker() as session:
            employer = (
                await session.exec(
                    select(Employer).options(joinedload(Employer.jobs)).where(Employer.id == employer_id))).first()
            if not employer:
                return UpdateEmployer(message="employer not found")
            if name is not None:
                employer.name = name
            if contact_email is not None:
                employer.contact_email = contact_email
            if industry is not None:
                employer.industry = industry
            await session.commit()
            await session.refresh(employer)
            return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)

    success = Boolean()
    message = String()

    @staticmethod
    async def mutate(root, info, employer_id):
        async with async_session_maker() as session:
            employer = (await session.exec(select(Employer).where(Employer.id == employer_id))).first()
            if not employer:
                return DeleteEmployer(success= False, message="employer not found")
            await session.delete(employer)
            await session.commit()
            return DeleteEmployer(success= True, message="employer deleted successfully")
