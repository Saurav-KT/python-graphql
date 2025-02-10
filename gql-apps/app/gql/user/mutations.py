

from graphene import Mutation, String, Int, Field, Boolean
from app.gql.types import JobObject
from app.db.database import AsyncSession
from app.db.models import Job

class LoginUser(Mutation):
    pass