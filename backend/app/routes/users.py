from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import os
import httpx
import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Load environment variables from .env file
load_dotenv()

# Supabase configurations
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define Pydantic models
class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: str
    tenant_id: str
    created_at: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_data: Optional[dict] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Create a router instance
router = APIRouter()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# Helper function to get headers
def get_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token_data

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

# Authentication endpoint
@router.post("/api/login", response_model=LoginResponse)
async def login_endpoint(user_data: UserLogin):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
                json={"email": user_data.email, "password": user_data.password},
                headers=get_headers()
            )

        print(f"Supabase auth response: {response.status_code}, {response.text}")  # Debugging: Print Supabase response

        if response.status_code == 200:
            user_info = response.json()
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_info["user"]["email"]}, expires_delta=access_token_expires
            )
            user_info["access_token"] = access_token
            user_info["token_type"] = "bearer"
            return LoginResponse(success=True, message="Login successful", user_data=user_info)
        else:
            return LoginResponse(success=False, message="Invalid credentials")

    except Exception as e:
        print(f"General error ({type(e).__name__}): {e}")
        return LoginResponse(success=False, message=f"{type(e).__name__}: {e}")

# Token endpoint
@router.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
                json={"email": form_data.username, "password": form_data.password},
                headers=get_headers()
            )

        print(f"Supabase token response: {response.status_code}, {response.text}")  # Debugging: Print Supabase response

        if response.status_code == 200:
            user_info = response.json()
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_info["user"]["email"]}, expires_delta=access_token_expires
            )
            return Token(access_token=access_token, token_type="bearer")
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        print(f"General error ({type(e).__name__}): {e}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")

# Read all users
@router.get("/users", response_model=List[User])
async def read_users(current_user: TokenData = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/users?select=*",
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Read specific user by id
@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str, current_user: TokenData = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}&select=*",
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()[0]
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Create a new user
@router.post("/users", response_model=User)
async def create_user(user: UserCreate, current_user: TokenData = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/users",
            json=user.dict(),
            headers=get_headers()
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Update an existing user
@router.patch("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserUpdate, current_user: TokenData = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
            json=user.dict(exclude_unset=True),
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Delete a user
@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: TokenData = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
            headers=get_headers()
        )
        if response.status_code == 204:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
