import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import SessionLocal
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = SessionLocal()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Add it to your .env file.")
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def create_token(username: str, expires: timedelta, token_type: str) -> str:
    payload = {
        "sub": username,
        "type": token_type,
        "exp": datetime.now(timezone.utc) + expires,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != expected_type:
        raise HTTPException(status_code=401, detail="Wrong token type")
    return payload["sub"]


def get_current_username(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    return decode_token(credentials.credentials, "access")


def get_refresh_username(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    return decode_token(credentials.credentials, "refresh")


@auth_router.get('/', summary="Auth health check")
async def hello():
    """
    A simple check that the auth router is running.
    """
    return {"message": "Hello World"}


@auth_router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account",
    responses={400: {"description": "Username or email already exists"}},
)
async def signup(user: SignUpModel):
    """
    Create a new user account.

    The request body needs:
    - **username**: must be unique
    - **email**: must be unique
    - **password**: stored as a salted hash, never as plain text
    - **is_staff**: whether the user is staff (optional, default false)
    - **is_active**: whether the account is active (optional, default true)
    """
    db_email = session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
        )

    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    return new_user


@auth_router.post(
    '/login',
    status_code=200,
    summary="Log in and get tokens",
    responses={400: {"description": "Invalid username or password"}},
)
async def login(user: LoginModel):
    """
    Log in with a username and password.

    Returns two JWT tokens:
    - **access_token**: valid for 30 minutes, used to call protected routes
    - **refresh_token**: valid for 7 days, used only at `/auth/refresh`

    Usernames are case-sensitive.
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = create_token(db_user.username, timedelta(minutes=30), "access")
        refresh_token = create_token(db_user.username, timedelta(days=7), "refresh")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password"
    )


@auth_router.get(
    '/me',
    summary="Get the logged-in username",
    responses={401: {"description": "Missing, expired or wrong-type token"}},
)
async def me(username: str = Depends(get_current_username)):
    """
    Return the username stored in the access token.

    Requires a valid **access token**. A refresh token is rejected.
    """
    return {"username": username}


@auth_router.get(
    '/refresh',
    summary="Get a new access token",
    responses={401: {"description": "Missing, expired or wrong-type token"}},
)
async def refresh(username: str = Depends(get_refresh_username)):
    """
    Exchange a refresh token for a new access token.

    Authorize with the **refresh token** (not the access token) before calling this.
    """
    return {"access_token": create_token(username, timedelta(minutes=30), "access")}