import hashlib
import hmac
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models import Survey, User, UserLogin, UserRegister


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # must be False when allow_origins is "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- password helpers ----------
def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 100_000
    ).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    salt, digest = stored.split("$")
    new_digest = hash_password(password, salt).split("$")[1]
    return hmac.compare_digest(new_digest, digest)


# ---------- routes ----------
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register")
async def user_register(data: UserRegister):
    username = data.username.strip()
    if not username or not data.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    if data.password != data.confirmed_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username is already taken")

        user = User(username=username, password=hash_password(data.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": "success", "message": "Account created", "username": user.username}


@app.post("/login")
async def user_login(data: UserLogin):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == data.username.strip())).first()
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Wrong username or password")
        return {"status": "success", "message": "Login successful", "username": user.username}


@app.get("/Survey/{id}")
async def read_survey(id: int):
    with Session(engine) as session:
        survey = session.get(Survey, id)
        return {"message": survey}


@app.post("/Survey")
async def create_survey(survey: Survey):
    with Session(engine) as session:
        session.add(survey)
        session.commit()
        session.refresh(survey)
        return {"status": "success", "message": survey}
