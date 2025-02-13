import datetime
import string
from random import choices

from graphene import Mutation, String
from graphql import GraphQLError

from app.db.database import async_session_maker
from app.db.models import User
from sqlmodel import select
from app.utils import generate_token, verify_password

class LoginUser(Mutation):
    class Arguments:
        email= String(required= True)
        password= String(required= True)

    token= String()

    @staticmethod
    async def mutate(root, info, email,password):
        async with async_session_maker() as session:
             user = (await session.exec(select(User).where(User.email == email))).first()
             if not user :
                 raise GraphQLError("A user by that email does not exist")

             verify_password(user.password_hash,password)

             # token = ''.join(choices(string.ascii_lowercase, k=10))
             token = generate_token(email)
             return LoginUser(token=token)
