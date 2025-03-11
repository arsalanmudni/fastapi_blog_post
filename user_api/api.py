from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db.session import SessionDep
from user_api.auth import get_password_hash, verify_password, create_access_token
from user_api.model import User
from user_api.schema import UserRegistration, UserOut, UserLogin

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/register")
async def register(user: UserRegistration, session: SessionDep):
    data = UserRegistration.dict(user)
    user_check = session.exec(select(User).where(User.username == data.get('username'))).first()
    email_check = session.exec(select(User).where(User.email == data.get('email'))).first()
    if user_check:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username '{data.get('username')}' already exists")
    if email_check:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email '{data.get('email')}' already exists")
    password = data.pop('password')
    hashed_password = get_password_hash(password)
    data["hash"] = hashed_password
    user_data = User(**data)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    response = UserOut.from_orm(user_data)
    return response


@user_router.post("/login")
async def login(user: UserLogin, session: SessionDep):
    data = UserLogin.dict(user)
    user = session.exec(select(User).where(User.username == data.get('username'))).first()
    verify_pass = verify_password(data.get('password'), user.hash) if user else False
    if not user or not verify_pass:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username and/or password incorrect")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
