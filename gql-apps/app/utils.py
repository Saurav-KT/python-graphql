import jwt
from datetime import datetime, timedelta,UTC
from app.settings.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRATION_TIME_MINUTES

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError

def generate_token(email):
    # now + token lifespan
    expiration_time = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload={
        "sub": email,
        "exp": expiration_time
    }
    token= jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)

def verify_password(pwd_hash, pwd):
    ph = PasswordHasher()
    try:
        ph.verify(pwd_hash, pwd)

    except VerifyMismatchError:
        raise GraphQLError("invalid password")
