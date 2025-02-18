import datetime
import string
from random import choices

from graphene import Mutation, String, Field, Int
from graphql import GraphQLError

from app.db.database import async_session_maker
from app.db.models import User, JobApplication
from sqlmodel import select
from app.utils import generate_token, verify_password, get_authenticated_user, auth_user_same_as
from app.gql.types import UserObject, JobApplicationObject
from app.utils import hash_password


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    async def mutate(root, info, email, password):
        async with async_session_maker() as session:
            user = (await session.exec(select(User).where(User.email == email))).first()
            if not user:
                raise GraphQLError("A user by that email does not exist")

            verify_password(user.password_hash, password)
            token = generate_token(email)
            return LoginUser(token=token)


class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)


    @staticmethod
    async def mutate(root, info, username, email, password, role):
        # to prevent a normal user to add admin user
        if role=="admin":
            current_user = await get_authenticated_user(info.context)
            if current_user.role != "admin":
                raise GraphQLError("Only admin user can add new admin")

        async with async_session_maker() as session:
            user = (await session.exec(select(User).where(User.email == email))).first()
            if user:
                raise GraphQLError("A user with that email already exist")
            password_hash = hash_password(password)
            user = User(username=username, email=email, password_hash=password_hash, role=role)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return AddUser(user=user)

class ApplyToJob(Mutation):
    class Arguments:
        user_id= Int(required= True)
        job_id= Int(required= True)


    job_application= Field(lambda: JobApplicationObject)

    @auth_user_same_as
    async def mutate(root, info, user_id,job_id):
        async with async_session_maker() as session:
            existing_application= (await session.exec(select(JobApplication).where(JobApplication.user_id == user_id, JobApplication.job_id==job_id))).first()
            if existing_application:
                raise GraphQLError("This user has already applied to this job")
            job_application= JobApplication(user_id=user_id,job_id= job_id)
            session.add(job_application)
            await session.commit()
            await session.refresh(job_application)
            return ApplyToJob(job_application=job_application)





