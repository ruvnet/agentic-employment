import uvicorn
import asyncio
import json
import httpx
import os
import uuid
import gradio as gr
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Define a Pydantic model for the login response
class LoginResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    user_data: Optional[dict] = None

# Define Pydantic model for user login data
class UserLogin(BaseModel):
    email: str
    password: str
    last_login: Optional[datetime] = None
    login_count: Optional[int] = 0
    session_id: Optional[str] = None
    session_start: Optional[datetime] = None
    session_end: Optional[datetime] = None

# Create a FastAPI app instance
app = FastAPI()

class AuthenticationError(Exception):
    pass

def authenticate_user(email, password):
    api_key = os.getenv("SUPABASE_API_KEY")
    if not api_key:
        raise ValueError("SUPABASE_API_KEY environment variable is not set")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = httpx.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["idToken"]
    elif response.status_code == 400:
        raise AuthenticationError("Invalid email or password")
    else:
        response.raise_for_status()

def generate_session_id():
    return str(uuid.uuid4())

def log_user_activity(user_email: str, activity: str, user_agent: str):
    sanitized_email = user_email.replace("@", "_").replace(".", "_")
    data = {
        "timestamp": datetime.now().isoformat(),
        "activity": activity,
        "user_agent": user_agent
    }
    supabase.table("logs").insert(data).execute()

# Define a route for the login endpoint
@app.post("/api/login", response_model=LoginResponse)
async def login_endpoint(request: Request, user_data: UserLogin):
    try:
        # Authenticate user with Supabase
        user = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Log user activity
        user_agent = request.headers.get("User-Agent")
        log_user_activity(user_data.email, "Login", user_agent)
        
        # Update user details
        user_data.last_login = datetime.now()
        user_data.login_count += 1
        user_data.session_id = generate_session_id()
        user_data.session_start = datetime.now()
        user_data.session_end = user_data.session_start + timedelta(hours=8)  # Set session duration to 8 hours

        # Save user details to Supabase
        sanitized_email = user_data.email.replace("@", "_").replace(".", "_")
        data = {
            "email": user_data.email,
            "last_login": user_data.last_login.isoformat(),
            "login_count": user_data.login_count,
            "session_id": user_data.session_id,
            "session_start": user_data.session_start.isoformat(),
            "session_end": user_data.session_end.isoformat()
        }
        supabase.table("users").upsert(data).execute()

        # Retrieve user data from Supabase
        user_data_snapshot = supabase.table("users").select("*").eq("email", user_data.email).execute()
        user_data_dict = user_data_snapshot.data[0] if user_data_snapshot.data else {}
        
        return LoginResponse(success=True, user_data=user_data_dict)
    except AuthenticationError as e:
        return LoginResponse(success=False, message=str(e))
    except httpx.HTTPStatusError as e:
        return LoginResponse(success=False, message=f"HTTP error occurred: {e.response.status_code}")
    except httpx.RequestError as e:
        return LoginResponse(success=False, message=f"An error occurred while requesting: {e}")
    except httpx.TimeoutException as e:
        return LoginResponse(success=False, message="The request timed out")
    except Exception as e:
        return LoginResponse(success=False, message=str(e))

# Serve Swagger UI HTML
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI"
    )

# (Optional) Serve OAuth2 redirect URL
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# Define the Gradio interface
def gradio_login():
    with gr.Blocks() as demo:
        # Setup components
        error_message = gr.Markdown(visible=False)
        username = gr.Textbox(label="Email")
        password = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        welcome_message = gr.Markdown(visible=False)
        
        # Define the main content area, initially hidden
        main_content = gr.Column(visible=False)

        # Content to be displayed after login
        with main_content:
            gr.Markdown("## 🦄 Welcome, you've logged in!")
            gr.Markdown("Good job!")

        def on_login_click(email, password):
            try:
                # Send a POST request to the FastAPI login endpoint
                response = httpx.post("http://localhost:8001/api/login", json={"email": email, "password": password})
                response.raise_for_status()
                login_response = response.json()
                if login_response["success"]:
                    user_data = login_response.get("user_data", {})
                    user_data_str = json.dumps(user_data, indent=2)
                    return (
                        gr.update(visible=True, value=f"Welcome! Login successful\n\nUser Data:\n{user_data_str}"),
                        gr.update(visible=False),
                        gr.update(visible=True),
                        gr.update(visible=True)
                    )
                else:
                    return (
                        gr.update(visible=True, value=login_response["message"]),
                        gr.update(visible=True),
                        gr.update(visible=True),
                        gr.update(visible=False)
                    )
            except httpx.HTTPStatusError as e:
                return (
                    gr.update(visible=True, value=f"HTTP error occurred: {e.response.status_code}"),
                    gr.update(visible=True),
                    gr.update(visible=True),
                    gr.update(visible=False)
                )
            except httpx.RequestError as e:
                return (
                    gr.update(visible=True, value=f"An error occurred while requesting: {e}"),
                    gr.update(visible=True),
                    gr.update(visible(True)),
                    gr.update(visible=False)
                )
            except httpx.TimeoutException as e:
                return (
                    gr.update(visible=True, value="The request timed out"),
                    gr.update(visible=True),
                    gr.update(visible(True)),
                    gr.update(visible(False))
                )
            except Exception as e:
                return (
                    gr.update(visible=True, value=f"An unexpected error occurred: {e}"),
                    gr.update(visible=True),
                    gr.update(visible(True)),
                    gr.update(visible(False))
                )

        # Binding the function to the button click
        login_button.click(on_login_click, inputs=[username, password], outputs=[welcome_message, error_message, main_content, login_button])

    return demo

# Run the FastAPI app
def run_fastapi_app():
    uvicorn.run(app, host="0.0.0.0", port=8001)

# Run the Gradio app
def run_gradio_app():
    gradio_app = gradio_login()
    gradio_app.launch()

if __name__ == "__main__":
    import multiprocessing

    fastapi_process = multiprocessing.Process(target=run_fastapi_app)
    gradio_process = multiprocessing.Process(target=run_gradio_app)

    fastapi_process.start()
    gradio_process.start()

    fastapi_process.join()
    gradio_process.join()
