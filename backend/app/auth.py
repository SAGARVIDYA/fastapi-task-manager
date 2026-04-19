from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta


SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# hash password
def hash_password(password: str):

    return pwd_context.hash(password)


# verify password
def verify_password(

        plain_password,
        hashed_password

):

    return pwd_context.verify(

        plain_password,
        hashed_password

    )


# create token
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(

        minutes=ACCESS_TOKEN_EXPIRE_MINUTES

    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(

        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM

    )

    return encoded_jwt


# verify token  ⭐ IMPORTANT
def verify_token(token: str):

    try:

        payload = jwt.decode(

            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]

        )

        return payload

    except JWTError:

        return None