from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional  # Add this import statement
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Define a Pydantic model for the login response
class LoginResponse(BaseModel):
    success: bool
    message: str
    user_data: Optional[dict] = None

# Define Pydantic model for user login data
class UserLogin(BaseModel):
    email: str
    password: str

# Create a FastAPI app instance
app = FastAPI()

@app.post("/api/login", response_model=LoginResponse)
async def login_endpoint(user_data: UserLogin):
    try:
        print(f"Received login request for email: {user_data.email}")  # Debugging: Print email

        # Authenticate user with Supabase
        user_response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })

        print(f"Supabase auth response: {user_response}")  # Debugging: Print Supabase response

        if not user_response or not user_response.user:
            return LoginResponse(success=False, message="Invalid credentials")

        user = user_response.user

        # Convert the user object to a dictionary for JSON serialization
        user_data_dict = {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
            "confirmed_at": user.confirmed_at.isoformat() if user.confirmed_at else None,
            "last_sign_in_at": user.last_sign_in_at.isoformat() if user.last_sign_in_at else None,
            "role": user.role,
            "updated_at": user.updated_at.isoformat(),
            "app_metadata": user.app_metadata,
            "user_metadata": user.user_metadata,
            "identities": [
                {
                    "id": identity.id,
                    "user_id": identity.user_id,
                    "identity_data": identity.identity_data,
                    "provider": identity.provider,
                    "created_at": identity.created_at.isoformat(),
                    "last_sign_in_at": identity.last_sign_in_at.isoformat() if identity.last_sign_in_at else None,
                    "updated_at": identity.updated_at.isoformat()
                } for identity in user.identities
            ]
        }

        return LoginResponse(success=True, message="Login successful", user_data=user_data_dict)
    except Exception as e:
        print(f"General error ({type(e).__name__}): {e}")  # Enhanced debugging: Print exception type and message
        return LoginResponse(success=False, message=f"{type(e).__name__}: {e}")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
