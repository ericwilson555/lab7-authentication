from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from database.session import get_session, create_tables
from models.user import User, UserCreate, UserResponse
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_active_user
)

app = FastAPI(title="HealthTrack API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    create_tables()


@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    # Check username
    existing = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    # Check email
    existing = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Hash password
    hashed = hash_password(user_data.password)

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name,
        role=user_data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/users/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    return current_user