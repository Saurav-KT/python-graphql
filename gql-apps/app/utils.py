from functools import wraps
from datetime import datetime, timedelta,UTC,timezone
import jwt
from app.settings.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRATION_TIME_MINUTES
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from app.db.database import async_session_maker
from sqlmodel import select
from app.db.models import User


def generate_token(email):
    # now + token lifespan
    expiration_time = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload={
        "sub": email,
        "exp": expiration_time
    }
    token= jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

async def get_authenticated_user(context):
    request_object = context.get('request')
    auth_header= request_object.headers.get('Authorization')
    token=[]
    if auth_header:
        token= auth_header.split(" ")
    if auth_header and token[0]=="Bearer" and len(token)==2:
        try:
            payload = jwt.decode(token[1], SECRET_KEY, algorithms=[ALGORITHM])
            if datetime.now(timezone.utc)> datetime.fromtimestamp(payload['exp'],tz=timezone.utc):
                raise GraphQLError('Token has expired')

            async with async_session_maker() as session:
                   user = (await session.exec(select(User).where(User.email == payload.get('sub')))).first()
                   if not user:
                       raise GraphQLError("Could not authenticate user")
                   return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError("Invalid authentication token")
        except Exception as e:
            raise GraphQLError("Could not authenticate user")
    else:
        raise GraphQLError("Missing authentication token")


def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)

def verify_password(pwd_hash, pwd):
    ph = PasswordHasher()
    try:
        ph.verify(pwd_hash, pwd)

    except VerifyMismatchError:
        raise GraphQLError("invalid password")

def admin_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info= args[1]
        user = await get_authenticated_user(info.context)
        if user.role != "admin":
            raise GraphQLError("you are not authorized to perform this action")
        result = await func(*args, *kwargs)
        return result
    return wrapper

def auth_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info= args[1]
        await get_authenticated_user(info.context)
        result = await func(*args, **kwargs)
        return result
    return wrapper

def auth_user_same_as(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info= args[1]
        user = await get_authenticated_user(info.context)
        uid= kwargs.get("user_id")
        if user.id != uid:
            raise GraphQLError("you are not authorized to perform this action")
        result = await func(*args, **kwargs)
        return result
    return wrapper





