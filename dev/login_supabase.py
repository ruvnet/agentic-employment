import os
import json
import gradio as gr
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Define the Gradio interface
def gradio_login():
    with gr.Blocks() as demo:
        # Setup components
        with gr.Column(visible=True) as login_box:
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
                # Authenticate user with Supabase
                user_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                print(f"Supabase auth response: {user_response}")  # Debugging: Print Supabase response

                if not user_response or not user_response.user:
                    return (
                        gr.update(visible=True, value="Invalid credentials"),  # Show error_message with invalid credentials
                        gr.update(visible=False),  # Hide main_content
                        gr.update(visible=True),  # Show error_message
                        gr.update(visible=True)  # Keep login_box visible
                    )

                user = user_response.user
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
                user_data_str = json.dumps(user_data_dict, indent=2)
                print("User Data:", user_data_str)  # Debugging: Print user data

                return (
                    gr.update(visible=True, value=f"Welcome! Login successful\n\nUser Data:\n{user_data_str}"),  # Show welcome_message
                    gr.update(visible=True),  # Show main_content
                    gr.update(visible=False),  # Hide error_message
                    gr.update(visible=False)  # Hide login_box
                )
            except Exception as e:
                print("Exception occurred:", e)  # Debugging: Print exception
                return (
                    gr.update(visible=True, value=f"An unexpected error occurred: {e}"),  # Show error_message with exception message
                    gr.update(visible=False),  # Hide main_content
                    gr.update(visible=True),  # Show error_message
                    gr.update(visible=True)  # Keep login_box visible
                )

        # Binding the function to the button click
        login_button.click(on_login_click, inputs=[username, password], outputs=[welcome_message, main_content, error_message, login_box])

        # Show and Hide buttons for the main content
        show_button = gr.Button("Show Content")
        hide_button = gr.Button("Hide Content")

        def show_content():
            return gr.update(visible=True), gr.update(visible=False)

        def hide_content():
            return gr.update(visible=False), gr.update(visible=True)

        show_button.click(show_content, [], [main_content, login_box])
        hide_button.click(hide_content, [], [main_content, login_box])

    return demo

# Run the Gradio app
def run_gradio_app():
    gradio_app = gradio_login()
    gradio_app.launch()

if __name__ == "__main__":
    run_gradio_app()
