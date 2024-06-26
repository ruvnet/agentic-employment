import gradio as gr
import pandas as pd
import random
from gradio_modal import Modal

def create_new_agent_wizard():
    with Modal(visible=False) as create_agent_modal:
        
        # Step 1: Basic Information
        gr.Markdown("### Step 1: Basic Information")
        agent_name = gr.Textbox(label="Agent Name", placeholder="Enter the name of the agent...")
        agent_type = gr.Dropdown(["Conversational", "Analytical", "Generative", "Retrieval-based"], label="Agent Type")

        # Step 2: Configuration
        gr.Markdown("### Step 2: Configuration")
        agent_description = gr.Textbox(label="Description", placeholder="Describe the agent's primary functions...")
        llm_choice = gr.Dropdown(["GPT-3.5", "GPT-4", "Claude", "Anthropic-100k", "Chinchilla", "PaLM"], label="Choose LLM Base")
        
        
        # Agent Description and Avatar
        gr.Markdown("#### Agent Description and Avatar")
        agent_description_input = gr.Textbox(label="Agent Description", placeholder="Enter agent description...")
        agent_avatar_input = gr.Image(type="filepath", label="Agent Avatar")
        
        # Agent LLM and Prompt
        gr.Markdown("#### Agent LLM and Prompt")
        agent_llm_dropdown = gr.Dropdown(["GPT-3.5", "GPT-4", "Claude", "Anthropic-100k", "Chinchilla", "PaLM", "Jurassic-2", "Bedrock", "Cohere", "Llama", "Alpaca", "Vicuna", "Falcon", "MPT", "Dolly", "StableLM", "RedPajama-INCITE", "OpenAssistant"], value="GPT-3.5", label="Agent LLM")
        agent_prompt_input = gr.Textbox(label="Agent Prompt", placeholder="Enter agent prompt...")
        
        # Agent Knowledge Base
        gr.Markdown("#### Agent Knowledge Base")
        agent_knowledge_upload = gr.File(label="Upload Agent Knowledge Base")
        agent_knowledge_url = gr.Textbox(label="Agent Knowledge URL", placeholder="Enter URL to agent knowledge base...")
        
        # Learning and Exploration Settings
        gr.Markdown("#### Learning and Exploration Settings")
        agent_learning_rate_slider = gr.Slider(0.0, 1.0, value=0.01, label="Learning Rate")
        agent_exploration_slider = gr.Slider(0.0, 1.0, value=0.1, label="Exploration Rate")
        
        # Training Settings
        gr.Markdown("#### Training Settings")
        agent_iterations_slider = gr.Slider(1, 100, value=10, step=1, label="Training Iterations")
        agent_batch_size_slider = gr.Slider(1, 256, value=32, step=1, label="Batch Size")
        
        # Output Settings
        gr.Markdown("#### Output Settings")
        agent_max_tokens_slider = gr.Slider(1, 4096, value=512, step=1, label="Max Tokens")
        agent_temperature_slider = gr.Slider(0.0, 1.0, value=0.7, label="Temperature")
        agent_top_p_slider = gr.Slider(0.0, 1.0, value=1.0, label="Top P")
        agent_frequency_penalty_slider = gr.Slider(0.0, 2.0, value=0.0, label="Frequency Penalty")
        agent_presence_penalty_slider = gr.Slider(0.0, 2.0, value=0.0, label="Presence Penalty")
        agent_stop_sequences_input = gr.Textbox(label="Stop Sequences", placeholder="Enter stop sequences (comma-separated)...")
        
        # Agent Control Buttons
        # gr.Markdown("#### Agent Control Buttons")
        # start_agent_button = gr.Button("Start Agent")
        # stop_agent_button = gr.Button("Stop Agent")
        
        # Agent Status and Performance
        gr.Markdown("#### Agent Status and Performance")
        agent_status_indicator = gr.Textbox(label="Agent Status", interactive=False)
        agent_performance_chart = gr.LinePlot(x="Iteration", y="Performance", label="Agent Performance")
    
        # Step 3: Advanced Settings
        gr.Markdown("### Step 3: Advanced Settings")
        training_data = gr.File(label="Upload Training Data")
        parameters = gr.Textbox(label="Model Parameters")
        
        # Step 4: Review and Create
        gr.Markdown("### Step 4: Review and Create")
        create_button = gr.Button("Create Agent")
        
        # Define the logic for creating an agent
        def create_agent(agent_name, agent_type, agent_description, llm_choice, training_data, parameters):
            return f"Agent '{agent_name}' of type '{agent_type}' created successfully with model '{llm_choice}'."
        
        create_button.click(
            create_agent,
            inputs=[agent_name, agent_type, agent_description, llm_choice, training_data, parameters],
            outputs=[gr.Markdown()]  # Output could be a status message or redirection to the agent list
        )
        
    return create_agent_modal

def settings_conversation(user_message, chat_history):
    bot_response = random.choice([
        "How can I assist you with settings?",
        "What would you like to change?",
        "I'm here to help with any settings issues!"
    ])
    chat_history.append((user_message, bot_response))
    return "", chat_history  # Clear the message input after submission
    
def agent_management():
    with gr.Blocks() as agent_dashboard:
        with gr.Row():
            create_agent_button = gr.Button("Create New Agent", elem_id="create_agent_button")
            view_agent_list_button = gr.Button("View Agent List", elem_id="view_agent_list_button")
            settings_button = gr.Button("Chat", elem_id="settings_button")

        create_agent_modal = create_new_agent_wizard()  # Instantiate the create agent wizard modal

        # Define the agent list
        agent_list = [
            [1, "Sales AI", "Conversational", "Active", 4.5],
            [2, "Support Bot", "Retrieval-based", "Active", 4.2],
            [3, "Marketing Assistant", "Generative", "Inactive", 3.8],
            [4, "Data Analyst", "Analytical", "Active", 4.7],
            [5, "HR Coordinator", "Conversational", "Active", 4.1]
        ]

        with Modal(visible=False) as view_agent_list_modal:
            gr.Markdown("### View Agent List")
            agent_table = gr.DataFrame(
                agent_list,
                headers=["ID", "Name", "Type", "Status", "Performance"],
                datatype=["number", "str", "str", "str", "number"],
                interactive=True,
                row_count=(5, "fixed")
            )
            agent_details = gr.HTML()

            def show_agent_details(agent_table_data):
                if agent_table_data is None or len(agent_table_data) == 0:
                    return "No agent selected."
                
                agent_id = agent_table_data[0]  # Assuming selection gives the first row
                agent = next((a for a in agent_list if a[0] == agent_id), None)
                if agent:
                    details = f"<b>Agent ID:</b> {agent[0]}<br>"
                    details += f"<b>Name:</b> {agent[1]}<br>"
                    details += f"<b>Type:</b> {agent[2]}<br>"
                    details += f"<b>Status:</b> {agent[3]}<br>"
                    details += f"<b>Performance:</b> {agent[4]}<br>"
                    # Add conditional task details here as per agent ID
                    return details
                else:
                    return "Agent not found."

        with Modal(visible=False) as settings_modal:
            gr.Markdown("### Settings Conversation")
            chat_history = []
            chatbot = gr.Chatbot(label="Chat with Settings Bot", value=chat_history)
            msg_input = gr.Textbox(label="Type your message here...", placeholder="Type here...")
            msg_input.submit(settings_conversation, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])

        # Button clicks to show modals
        create_agent_button.click(lambda: Modal(visible=True), None, create_agent_modal)
        view_agent_list_button.click(lambda: Modal(visible=True), None, view_agent_list_modal)
        settings_button.click(lambda: Modal(visible=True), None, settings_modal)

        with gr.Accordion("Agent Dashboard"):
            with gr.Row():
                timeframe = gr.Dropdown(["Last 24 hours", "Last 7 days", "Last 30 days", "Custom Range"], value="Last 7 days", label="Timeframe")
                agent_groups = gr.Dropdown(["All Groups", "Sales", "Support", "Marketing"], value="All Groups", label="Agent Groups")
                llms = gr.Dropdown(["All LLMs", "GPT-3.5", "GPT-4", "Claude", "Anthropic-100k", "Chinchilla", "PaLM", "Jurassic-2", "Bedrock", "Cohere", "Llama", "Alpaca", "Vicuna", "Falcon", "MPT", "Dolly", "StableLM", "RedPajama-INCITE", "OpenAssistant"], value="All LLMs", label="LLMs")
                customizations = gr.Dropdown(["Default", "High Performance", "Cost Optimized"], value="Default", label="Customizations")

            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("## Agent Workforce Overview")
                    total_agents = gr.Number(value=500, label="Total Agents")
                    active_agents = gr.Number(value=375, label="Active Agents") 
                    idle_agents = gr.Number(value=125, label="Idle Agents")
                with gr.Column(scale=1):
                    gr.Markdown("## Agent Performance")
                    total_tasks = gr.Number(value=12500, label="Total Tasks Completed")
                    avg_duration = gr.Number(value=25.6, label="Avg. Task Duration (min)")
                    agent_rating = gr.Number(value=4.7, label="Avg. Agent Rating (out of 5)")

            with gr.Row():
                with gr.Column(scale=1):  
                    gr.Markdown("## Resource Utilization")
                    compute_usage = gr.Number(value=85.2, label="Compute Usage (%)")
                    storage_usage = gr.Number(value=1250, label="Storage Usage (GB)")
                    llm_calls = gr.Number(value=9875, label="Total LLM API Calls")  
                with gr.Column(scale=1):
                    gr.Markdown("## Cost Analysis") 
                    total_cost = gr.Number(value=12345.67, label="Total Cost ($)")
                    cost_per_task = gr.Number(value=0.99, label="Avg. Cost per Task ($)")
                    budget_remaining = gr.Number(value=54321.33, label="Budget Remaining ($)")

        with gr.Accordion("Agent List"):
            agent_list = [
                [1, "Sales AI", "Conversational", "Active", 4.5],
                [2, "Support Bot", "Retrieval-based", "Active", 4.2],
                [3, "Marketing Assistant", "Generative", "Inactive", 3.8],
                [4, "Data Analyst", "Analytical", "Active", 4.7],
                [5, "HR Coordinator", "Conversational", "Active", 4.1]
            ]

            agent_table = gr.DataFrame(
                agent_list,
                headers=["ID", "Name", "Type", "Status", "Performance"],
                datatype=["number", "str", "str", "str", "number"],
                col_count=(5, "fixed"),
                row_count=(5, "fixed"),
            )

            
    return agent_dashboard