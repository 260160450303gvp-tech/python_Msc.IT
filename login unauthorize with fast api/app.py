from fastapi import FastAPI, HTTPException, Depends, status, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import jwt
from datetime import datetime, timedelta, timezone


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="JWT Cookie Authentication with Database"
)


# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = "gggggj6yt6o"
ALGORITHM = "HS256"

# Token valid for 3 hours
TOKEN_EXPIRE_HOURS = 3


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ============================================================
# USER DATABASE MODEL
# ============================================================

class UserDB(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(100),
        nullable=False
    )

    full_name = Column(
        String(150),
        nullable=False
    )


# ============================================================
# CREATE DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# PYDANTIC MODELS
# ============================================================

class UserSignup(BaseModel):

    username: str
    password: str
    full_name: str


class UserLogin(BaseModel):

    username: str
    password: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {

        "message": "Welcome to JWT Authentication API",

        "status": "API is running successfully",

        "database": "SQLite",

        "login": "/login",

        "signup": "/signup",

        "profile": "/profile",

        "logout": "/logout",

        "docs": "/docs"
    }


# ============================================================
# 1. SIGNUP
# ============================================================

@app.post("/signup")
def signup(user: UserSignup):

    db = SessionLocal()

    try:

        # Check username
        existing_user = db.query(UserDB).filter(
            UserDB.username == user.username
        ).first()

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        # Create new user
        new_user = UserDB(

            username=user.username,

            password=user.password,

            full_name=user.full_name
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return {

            "message": "User created successfully",

            "id": new_user.id,

            "username": new_user.username,

            "full_name": new_user.full_name
        }

    finally:

        db.close()


# ============================================================
# 2. LOGIN
# ============================================================

@app.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    try:

        # Find user from database
        db_user = db.query(UserDB).filter(
            UserDB.username == user.username
        ).first()

        # User not found
        if not db_user:

            raise HTTPException(

                status_code=401,

                detail="Invalid username or password"
            )

        # Password check
        if user.password != db_user.password:

            raise HTTPException(

                status_code=401,

                detail="Invalid username or password"
            )

        # Token expiration = 3 hours
        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            hours=TOKEN_EXPIRE_HOURS
        )

        # JWT payload
        payload = {

            "sub": db_user.username,

            "name": db_user.full_name,

            "exp": expire
        }

        # Generate JWT
        token = jwt.encode(

            payload,

            SECRET_KEY,

            algorithm=ALGORITHM
        )

        # Response
        response = JSONResponse(

            content={

                "message": "Login successful",

                "username": db_user.username,

                "expires_in": "3 hours"
            }
        )

        # Store JWT in Cookie
        response.set_cookie(

            key="access_token",

            value=token,

            # Cookie valid for 3 hours
            max_age=3 * 60 * 60,

            # Cookie expiry
            expires=3 * 60 * 60,

            # JavaScript cannot access
            httponly=True,

            # Local development
            secure=False,

            # CSRF protection
            samesite="lax"
        )

        return response

    finally:

        db.close()


# ============================================================
# 3. GET CURRENT USER FROM COOKIE
# ============================================================

def get_current_user(

    access_token: str | None = Cookie(
        default=None
    )

):

    # Cookie not found
    if not access_token:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Unauthorized access. Please login first."
        )

    try:

        # Decode JWT
        payload = jwt.decode(

            access_token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        # Get username
        username = payload.get("sub")

        if username is None:

            raise HTTPException(

                status_code=401,

                detail="Invalid token. Please login again."
            )

        # Database connection
        db = SessionLocal()

        try:

            # Find user
            user = db.query(UserDB).filter(

                UserDB.username == username

            ).first()

            if not user:

                raise HTTPException(

                    status_code=401,

                    detail="User not found. Please login again."
                )

            return {

                "id": user.id,

                "username": user.username,

                "full_name": user.full_name
            }

        finally:

            db.close()

    # Token expired
    except jwt.ExpiredSignatureError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Token expired. Please login again."
        )

    # Invalid token
    except jwt.InvalidTokenError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token. Please login again."
        )


# ============================================================
# 4. PROTECTED PROFILE
# ============================================================

@app.get("/profile")
def get_profile(

    current_user: dict = Depends(
        get_current_user
    )

):

    return {

        "message": "Authentication successful!",

        "id": current_user["id"],

        "username": current_user["username"],

        "full_name": current_user["full_name"],

        "status": "You are authorized"
    }


# ============================================================
# 5. LOGOUT
# ============================================================

@app.post("/logout")
def logout():

    response = JSONResponse(

        content={

            "message": "Logout successful",

            "status": "Cookie deleted"
        }
    )

    # Delete JWT cookie
    response.delete_cookie(

        key="access_token",

        httponly=True,

        samesite="lax"
    )

    return response


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        app,

        host="127.0.0.1",

        port=8000
    )