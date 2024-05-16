To authenticate users in your FastAPI application and secure your routes, you'll need to implement JWT (JSON Web Token) authentication. Here’s a step-by-step guide to setting up and using JWT authentication in your FastAPI application.

### Step 1: Install Required Packages

Make sure you have `fastapi`, `httpx`, and `python-jose` installed:

```sh
pip install fastapi httpx python-jose python-dotenv
```

### Step 2: Create the Authentication Utilities

Create a file `backend/app/utils/auth.py` for the authentication utilities. This will handle JWT encoding and decoding.

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime, timedelta

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class User(BaseModel):
    email: str

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    # Implement your password hashing and verification logic here
    return plain_password == hashed_password  # This is just for demonstration

def get_user(email: str):
    # Replace this with your database call to get the user
    if email == "test@example.com":
        return UserInDB(**{
            "email": email,
            "hashed_password": "fakehashedpassword"
        })
    return None

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
```

### Step 3: Create the Token Endpoint

Create a token endpoint in `backend/app/routes/users.py` to handle user authentication and token generation.

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.app.utils.auth import authenticate_user, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### Step 4: Protect Your Routes

Update the `users.py` file to protect the routes using the authentication utilities.

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
from dotenv import load_dotenv
from backend.app.utils.auth import get_current_user, TokenData

# Load environment variables from .env file
load_dotenv()

# Supabase configurations
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Define Pydantic models
class UserBase(BaseModel):
    email: str
    role: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: str
    tenant_id: str
    created_at: str

# Create a router instance
router = APIRouter()

# Helper function to get headers
def get_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

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
```

### Step 5: Update `main.py`

Ensure that the `main.py` file includes the `users` router and properly initializes the application:

```python
from fastapi import FastAPI
from backend.app.routes import agent, settings, users  # Import the users router

app = FastAPI()

app.include_router(agent.router)
app.include_router(settings.router)
app.include_router(users.router)  # Include the users router

@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic Employment Infrastructure Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 6: Obtain and Use the Token

To authenticate, you need to obtain a token by sending a POST request to `/token` endpoint with your credentials.

```sh
curl -X POST "http://localhost:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=fakehashedpassword"
```

The response will contain the JWT token, which you can use to authenticate subsequent requests:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

For example, to access the `/users` endpoint:

```sh
curl -X GET "http://localhost:8000/users