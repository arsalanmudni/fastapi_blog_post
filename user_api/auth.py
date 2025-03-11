from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.middleware.base import BaseHTTPMiddleware

from core.configs import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
EXEMPT_PATHS = ["/docs", "/openapi.json", "/user/register", "/user/login"]

oauth2_scheme
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_token_from_request(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = auth_header.split(" ")[1]  # Extract token after "Bearer"
    return token


def verify_access_token(request):
    # Extract the token from the request
    token = get_token_from_request(request)

    try:
        # Decode and verify the token using the secret key and algorithm
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Raise an HTTPException with status code 401 if the token has expired
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        # Raise an HTTPException with status code 401 if the token is invalid
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt



class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)
        try:
            # Call the verify_access_token function to validate the token
            verify_access_token(request)
            # If token validation succeeds, continue to the next middleware or route handler
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # If token validation fails due to HTTPException, return the error response
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            # If token validation fails due to other exceptions, return a generic error response
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)