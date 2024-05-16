import gradio as gr

def show_content():
    # This function makes the content area visible
    return gr.update(visible=True)

def hide_content():
    # This function hides the content area
    return gr.update(visible=False)

with gr.Blocks() as demo:
    with gr.Row():
        show_button = gr.Button("Show Content")
        hide_button = gr.Button("Hide Content")
    
    # Initially hidden content area
    content_area = gr.Markdown("This is the content area that can be shown or hidden.", visible=False)
    
    # Set the buttons to show or hide the content area
    show_button.click(show_content, [], content_area)
    hide_button.click(hide_content, [], content_area)

# Launch the Gradio app
demo.launch()
