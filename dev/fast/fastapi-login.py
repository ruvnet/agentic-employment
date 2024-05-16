import gradio as gr
import httpx
import json

def gradio_login():
    with gr.Blocks() as demo:
        # Setup components
        with gr.Column(visible=True) as login_box:
            error_message = gr.Markdown(visible=False)
            username = gr.Textbox(label="Email", placeholder="Enter your email")
            password = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
            login_button = gr.Button("Login")
            welcome_message = gr.Markdown(visible=False)
        
        # Define the main content area, initially hidden
        main_content = gr.Column(visible=False)

        # Content to be displayed after login
        with main_content:
            gr.Markdown("## 🦄 Welcome, you've logged in!")
            gr.Markdown("Good job!")
            user_info = gr.Markdown()

        def on_login_click(email, password):
            try:
                # Send a POST request to the FastAPI login endpoint
                response = httpx.post("http://localhost:8001/api/login", json={"email": email, "password": password})
                response.raise_for_status()
                login_response = response.json()
                
                print("Login Response:", login_response)  # Debugging: Print login response

                if login_response["success"]:
                    user_data = login_response.get("user_data", {})
                    user_data_str = json.dumps(user_data, indent=2)  # Correctly use json.dumps
                    print("User Data:", user_data_str)  # Debugging: Print user data
                    return (
                        gr.update(visible=True, value=f"Welcome! Login successful\n\nUser Data:\n{user_data_str}"),  # Show welcome_message
                        gr.update(visible=True),  # Show main_content
                        gr.update(visible=False),  # Hide error_message
                        gr.update(visible=False),  # Hide login_box
                        gr.update(value=f"User Data:\n{user_data_str}")  # Display user data
                    )
                else:
                    print("Login failed:", login_response["message"])  # Debugging: Print error message
                    return (
                        gr.update(visible=True, value=login_response["message"]),  # Show error_message with login response message
                        gr.update(visible(False)),  # Hide main_content
                        gr.update(visible(True)),  # Show error_message
                        gr.update(visible(True))  # Keep login_box visible
                    )
            except Exception as e:
                print("Exception occurred:", e)  # Debugging: Print exception
                return (
                    gr.update(visible(True, value=f"An unexpected error occurred: {e}")),  # Show error_message with exception message
                    gr.update(visible(False)),  # Hide main_content
                    gr.update(visible(True)),  # Show error_message
                    gr.update(visible(True))  # Keep login_box visible
                )

        # Binding the function to the button click
        login_button.click(on_login_click, inputs=[username, password], outputs=[welcome_message, main_content, error_message, login_box, user_info])

        # Show and Hide buttons for the main content
        show_button = gr.Button("Show Content")
        hide_button = gr.Button("Hide Content")

        def show_content():
            return gr.update(visible(True)), gr.update(visible(False))

        def hide_content():
            return gr.update(visible(False)), gr.update(visible(True))

        show_button.click(show_content, [], [main_content, login_box])
        hide_button.click(hide_content, [], [main_content, login_box])

    return demo

# Run the Gradio app
if __name__ == "__main__":
    gradio_app = gradio_login()
    gradio_app.launch()
