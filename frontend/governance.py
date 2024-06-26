import gradio as gr



def governance():
  with gr.Accordion("Governance Controls"):
    with gr.Tab("Boundaries & Constraints"):
        boundary_types = ["Ethical", "Legal", "Operational", "Financial", "Reputational"]
        boundary_table = gr.DataFrame(
            value=[
                ["Ethical", "Ensure agents adhere to company values and principles", "Active"],
                ["Legal", "Comply with all relevant laws and regulations", "Active"],
                ["Operational", "Maintain service level agreements and uptime targets", "Active"],
                ["Financial", "Stay within allocated budgets and resource limits", "Warning"],
                ["Reputational", "Protect company brand and public image", "Active"]
            ],
            headers=["Boundary Type", "Description", "Status"],
            row_count=5,
        )
        
        boundary_name_input = gr.Textbox(label="Boundary Name")
        boundary_type_dropdown = gr.Dropdown(boundary_types, label="Boundary Type")
        boundary_description_input = gr.Textbox(label="Boundary Description")
        add_boundary_button = gr.Button("Add Boundary")
        
        def add_boundary(name, boundary_type, description, boundary_table):
            boundary_table.append([name, boundary_type, description, "Active"])
            return boundary_table
        
        add_boundary_button.click(add_boundary, inputs=[boundary_name_input, boundary_type_dropdown, boundary_description_input, boundary_table], outputs=boundary_table)
        
    with gr.Tab("Human Feedback"):
        feedback_types = ["Approval", "Rejection", "Modification", "Clarification"]
        feedback_table = gr.DataFrame(
            value=[
                ["Sales AI", "Generated product description", "Approval", "Great job, the description is accurate and compelling"],
                ["Support Bot", "Handled customer complaint", "Modification", "The response was a bit too formal, try to be more empathetic"],
                ["Marketing Assistant", "Created ad campaign", "Clarification", "What is the target audience for this campaign?"],
                ["Data Analyst", "Provided sales forecast", "Approval", "The forecast looks solid, well done"],
                ["HR Coordinator", "Sent onboarding email", "Rejection", "The email contains outdated information, please update"]
            ],
            headers=["Agent", "Task", "Feedback Type", "Feedback Details"],
            row_count=5,
        )
        
        agent_dropdown = gr.Dropdown(["Sales AI", "Support Bot", "Marketing Assistant", "Data Analyst", "HR Coordinator"], label="Agent")
        task_input = gr.Textbox(label="Task")
        feedback_type_dropdown = gr.Dropdown(feedback_types, label="Feedback Type")
        feedback_details_input = gr.Textbox(label="Feedback Details")
        submit_feedback_button = gr.Button("Submit Feedback")
        
        def submit_feedback(agent, task, feedback_type, details, feedback_table):
            feedback_table.append([agent, task, feedback_type, details])
            return feedback_table
        
        submit_feedback_button.click(submit_feedback, inputs=[agent_dropdown, task_input, feedback_type_dropdown, feedback_details_input, feedback_table], outputs=feedback_table)
        
    with gr.Tab("Output Review"):
        review_status_options = ["Pending", "Approved", "Rejected"]
        output_review_table = gr.DataFrame(
            value=[
                ["Blog post", "Top 10 AI Trends for 2025", "Marketing Assistant", "Pending"],
                ["Financial report", "Q3 2024 Earnings Analysis", "Data Analyst", "Approved"],
                ["Product design", "Smartwatch UI Mockups", "Design AI", "Rejected"],
                ["Customer email", "Response to Billing Inquiry", "Support Bot", "Approved"],
                ["News article", "Company Announces New AI Partnership", "Content Creator", "Pending"]
            ],  
            headers=["Output Type", "Output Name", "Agent", "Review Status"],
            row_count=5,
        )
        
        output_type_input = gr.Textbox(label="Output Type")
        output_name_input = gr.Textbox(label="Output Name")  
        agent_dropdown = gr.Dropdown(["Sales AI", "Support Bot", "Marketing Assistant", "Data Analyst", "HR Coordinator", "Design AI", "Content Creator"], label="Agent")
        review_status_dropdown = gr.Dropdown(review_status_options, label="Review Status")
        submit_review_button = gr.Button("Submit Review")
        
        def submit_review(output_type, output_name, agent, review_status, output_review_table):
            output_review_table.append([output_type, output_name, agent, review_status])
            return output_review_table
        
        submit_review_button.click(submit_review, inputs=[output_type_input, output_name_input, agent_dropdown, review_status_dropdown, output_review_table], outputs=output_review_table)
        
    with gr.Tab("Alerts & Notifications"):
        alert_types = ["Boundary Violation", "Anomalous Behavior", "System Error", "Human Feedback Required"]
        alert_urgency_levels = ["Low", "Medium", "High", "Critical"]  
        alert_table = gr.DataFrame(
            value=[
                ["Boundary Violation", "Sales AI attempted to access restricted data", "High", "Unresolved"],
                ["Anomalous Behavior", "Support Bot response time increased by 150%", "Medium", "Under Investigation"],
                ["System Error", "Marketing Assistant encountered a memory leak", "Critical", "Resolved"], 
                ["Human Feedback Required", "Data Analyst report requires manager approval", "Low", "Pending"],
                ["Boundary Violation", "HR Coordinator tried to modify employee records without authorization", "High", "Unresolved"]
            ],
            headers=["Alert Type", "Description", "Urgency", "Status"], 
            row_count=5,
        )
        
        alert_type_dropdown = gr.Dropdown(alert_types, label="Alert Type")
        alert_description_input = gr.Textbox(label="Alert Description")
        alert_urgency_dropdown = gr.Dropdown(alert_urgency_levels, label="Alert Urgency")
        alert_status_input = gr.Textbox(label="Alert Status", value="Unresolved", interactive=False)
        create_alert_button = gr.Button("Create Alert")
        
        def create_alert(alert_type, description, urgency, status, alert_table):
            alert_table.append([alert_type, description, urgency, status])
            return alert_table
        
        create_alert_button.click(create_alert, inputs=[alert_type_dropdown, alert_description_input, alert_urgency_dropdown, alert_status_input, alert_table], outputs=alert_table)

  return gr.Column()