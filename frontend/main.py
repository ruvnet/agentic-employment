import gradio as gr
from agent_management import agent_management
from agent_controls import agent_controls
from collaboration_governance import collaboration_governance
from governance import governance
from analytics_reporting import analytics_reporting
from system_settings import system_settings
from documentation import documentation


with gr.Blocks() as app:
    documentation()

with gr.Blocks() as agentic_dashboard:
  gr.Markdown("# 🪰 Agentic Employment Infrastructure")
  gr.Markdown("### Manage an adaptive network of autonomous agents")

  with gr.Tab("Agent Management"):
    agent_management()

  with gr.Tab("Agentic Command & Control"):
    agent_controls()

  with gr.Tab("Collaboration & Governance"):
    collaboration_governance()

  with gr.Tab("Governance"):
    governance()

  with gr.Tab("Analytics & Reporting"):
    analytics_reporting()
      
  with gr.Tab("System Settings"):
    system_settings()

  with gr.Tab("Documentation"):
    documentation()  

# Launch the interface
agentic_dashboard.launch(debug=True)