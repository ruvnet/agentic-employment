import gradio as gr

def system_settings():
    with gr.Accordion("System Wide Settings"):
        with gr.Tab("Agent Parameters"):
            gr.Markdown("### Agent Parameters")
            gr.Markdown("Configure global parameters that affect all agents within the system.")
            
            with gr.Row():
                default_learning_rate = gr.Slider(minimum=0.01, maximum=1.0, value=0.1, step=0.01, label="Default Learning Rate")
                default_exploration_rate = gr.Slider(minimum=0.01, maximum=1.0, value=0.1, step=0.01, label="Default Exploration Rate")
            
            with gr.Row():
                agent_types = gr.CheckboxGroup(choices=["Conversational", "Retrieval-based", "Generative", "Analytical"], value=["Conversational", "Retrieval-based"], label="Agent Types")
                agent_specializations = gr.CheckboxGroup(choices=["Sales", "Support", "Marketing", "Data Analysis", "HR"], value=["Sales", "Support"], label="Agent Specializations")
            
            with gr.Row():
                reward_structure = gr.Radio(choices=["Fixed", "Variable", "Performance-based"], value="Fixed", label="Reward Structure")
                max_tokens = gr.Number(value=512, label="Max Tokens per Response")
            
        with gr.Tab("Resource Management"):
            gr.Markdown("### Resource Management")
            gr.Markdown("Manage compute resources and cost controls for the agent system.")
            
            with gr.Row():
                max_compute_usage = gr.Number(value=10000, label="Max Compute Usage (vCPU hours)")
                max_storage_usage = gr.Number(value=1000, label="Max Storage Usage (GB)")
            
            with gr.Row():
                cost_per_compute_hour = gr.Number(value=0.05, label="Cost per Compute Hour ($)")
                cost_per_gb_storage = gr.Number(value=0.02, label="Cost per GB Storage ($)")
            
        with gr.Tab("Access & Permissions"):
            gr.Markdown("### Access & Permissions")
            gr.Markdown("Configure access levels and permissions for users interacting with the agent system.")
            
            with gr.Row():
                user_roles = gr.CheckboxGroup(choices=["Administrator", "Developer", "Analyst", "Viewer"], value=["Administrator", "Developer"], label="User Roles")
                enable_api_access = gr.Checkbox(label="Enable API Access", value=True)
            
            with gr.Row():
                api_rate_limit = gr.Number(value=1000, label="API Rate Limit (requests/day)")
                enable_logging = gr.Checkbox(label="Enable Activity Logging", value=True)
            
    return gr.Column()
