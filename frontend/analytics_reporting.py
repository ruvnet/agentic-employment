import gradio as gr
import pandas as pd
import numpy as np
import plotly.express as px

def analytics_reporting():
    with gr.Accordion("Key Metrics", open=True):
        # Sample data
        dates = ["2023-01-01", "2023-01-08", "2023-01-15", "2023-01-22", "2023-01-29",
                 "2023-02-05", "2023-02-12", "2023-02-19", "2023-02-26", "2023-03-05",
                 "2023-03-12", "2023-03-19", "2023-03-26", "2023-04-02", "2023-04-09"]
        total_agents = [500, 525, 540, 560, 575, 590, 600, 615, 630, 645, 660, 675, 690, 700, 710]
        active_agents = [375, 395, 410, 430, 445, 460, 475, 490, 505, 520, 535, 550, 565, 580, 595]
        tasks_completed = [8000, 8500, 9200, 9800, 10400, 11000, 11600, 12200, 12800, 13400, 14000, 14600, 15200, 15800, 16400]
        avg_rating = [4.5, 4.52, 4.54, 4.56, 4.58, 4.6, 4.62, 4.64, 4.66, 4.68, 4.7, 4.72, 4.74, 4.76, 4.78]

        agent_metrics = {
            "Date": dates,
            "Total Agents": total_agents,
            "Active Agents": active_agents,
            "Tasks Completed": tasks_completed,
            "Avg Rating": avg_rating
        }

        agent_teams = {
            "Team": ["Sales", "Support", "Marketing", "Analytics", "HR"],
            "Agents": [120, 180, 95, 65, 40],
            "Tasks": [3200, 4800, 2400, 1600, 800],
            "Avg Rating": [4.7, 4.75, 4.65, 4.8, 4.72]
        }

        with gr.Row():
            with gr.Column():
                fig1 = px.line(agent_metrics, x='Date', y=['Total Agents', 'Active Agents'], title='Agent Workforce Metrics Over Time')
                plot1 = gr.Plot(fig1)
            with gr.Column():
                fig2 = px.line(agent_metrics, x='Date', y='Tasks Completed', title='Tasks Completed Over Time')
                plot2 = gr.Plot(fig2)

        with gr.Row():
            with gr.Column():
                fig3 = px.bar(agent_metrics, x='Date', y='Avg Rating', title='Average Agent Rating Over Time')
                plot3 = gr.Plot(fig3)
            with gr.Column():
                fig4 = px.bar(agent_teams, x='Team', y=['Agents', 'Tasks'], barmode='group', title='Agent Performance by Team')
                plot4 = gr.Plot(fig4)

        # Additional example
        with gr.Row():
          with gr.Column():
              fig5 = px.scatter(agent_metrics, x='Tasks Completed', y='Avg Rating', color='Active Agents', title='Correlation Between Tasks Completed, Rating, and Active Agents')
              plot5 = gr.Plot(fig5)
          with gr.Column():
              fig6 = px.pie(agent_teams, values='Agents', names='Team', title='Agent Distribution by Team')
              plot6 = gr.Plot(fig6)

    with gr.Accordion("Reporting", open=True):
      with gr.Tab("Custom Reports"):
            report_types = ["Agent Activities", "Agent Outputs", "Quality Levels"]
            report_type_dropdown = gr.Dropdown(report_types, value="Agent Activities", label="Report Type")
            
            report_period = ["Last 7 Days", "Last 30 Days", "Last 6 Months", "Last Year", "Custom Range"]
            report_period_dropdown = gr.Dropdown(report_period, value="Last 30 Days", label="Report Period")
            
            start_date_input = gr.Textbox(label="Start Date (YYYY-MM-DD)")
            end_date_input = gr.Textbox(label="End Date (YYYY-MM-DD)")
            
            generate_report_button = gr.Button("Generate Report")
            
            report_output = gr.DataFrame(
                value=[
                    ["Sales AI", 1250, 85, 4.7],
                    ["Support Bot", 2100, 92, 4.8],
                    ["Marketing Assistant", 875, 78, 4.5],
                    ["Data Analyst", 625, 90, 4.9],
                    ["HR Coordinator", 375, 82, 4.6]
                ],
                headers=["Agent", "Tasks Completed", "Success Rate (%)", "Avg Rating"],
                row_count=5,
            )
          
      with gr.Tab("Forecasting"):
          forecast_metrics = ["Total Agents", "Active Agents", "Tasks Completed", "Avg Rating"]
          forecast_metric_dropdown = gr.Dropdown(forecast_metrics, value="Tasks Completed", label="Forecast Metric")
          
          forecast_period = ["Next 7 Days", "Next 30 Days", "Next 6 Months", "Next Year"]
          forecast_period_dropdown = gr.Dropdown(forecast_period, value="Next 30 Days", label="Forecast Period")
          
          forecast_button = gr.Button("Generate Forecast")
          
          forecast_plot = gr.LinePlot(x="Date", y="Value", title="Forecast for Tasks Completed")
          
          def generate_report(report_type, report_period, start_date, end_date):
              # Placeholder logic to generate custom report based on selected parameters
              return report_output
          
          def generate_forecast(metric, period):
              # Placeholder logic to generate forecast based on selected parameters
              dates = pd.date_range(start='2023-01-01', end='2023-06-01', freq='W')
              values = np.random.randint(10000, 20000, size=len(dates))
              forecast_data = pd.DataFrame({"Date": dates, "Value": values})
              forecast_plot.plot(forecast_data, x="Date", y="Value", title=f"Forecast for {metric} ({period})")
      
      generate_report_button.click(generate_report, inputs=[report_type_dropdown, report_period_dropdown, start_date_input, end_date_input], outputs=report_output)
      forecast_button.click(generate_forecast, inputs=[forecast_metric_dropdown, forecast_period_dropdown], outputs=forecast_plot)    
      
      
    return gr.Column(plot1, plot2, plot3, plot4, plot5, plot6)