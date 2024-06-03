import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

# Sample Data
data = {
    'Year': [2020, 2021, 2022],
    'Carbon Footprint': [10, 9, 8],
    'Renewable Energy Usage': [20, 25, 30],
    'Water Usage': [50, 45, 40],
    'Employee Satisfaction': [70, 75, 80],
    'Board Diversity': [30, 35, 40]
}

df = pd.DataFrame(data)

def plot_metrics(metric):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Year'], df[metric], marker='o')
    plt.title(f'{metric} Over Years')
    plt.xlabel('Year')
    plt.ylabel(metric)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('/tmp/plot.png')
    return '/tmp/plot.png'

# Define functions for each section
def overview():
    overview_text = """
    ## Overview Dashboard
    - **Sustainability Score:** Composite score reflecting the overall ESG performance.
    - **Environmental Impact:** Carbon footprint, energy consumption, waste management.
    - **Social Impact:** Community engagement, diversity and inclusion statistics, employee well-being.
    - **Governance Metrics:** Board diversity, executive pay ratio, transparency, regulatory compliance.
    """
    return overview_text

def detailed_analysis():
    detailed_text = """
    ## Detailed ESG Analysis
    - **Environmental Metrics:** Greenhouse gas emissions, renewable energy usage, water usage, pollution levels.
    - **Social Metrics:** Employee satisfaction surveys, gender and ethnicity breakdowns, safety incidents.
    - **Governance Metrics:** Board structure, audit practices, anti-corruption measures, shareholder rights.
    """
    return detailed_text

def benchmarking_tools():
    benchmarking_text = """
    ## Benchmarking Tools
    - **Industry Comparisons:** Compare ESG performance against industry averages or specific competitors.
    - **Historical Trends:** Track changes in ESG metrics over time to identify trends and improvements.
    """
    return benchmarking_text

def risk_assessment():
    risk_text = """
    ## Risk Assessment
    - **Climate Risk:** Analyze the potential impact of climate change on the business.
    - **Reputation Risk:** Monitor social media and news outlets for mentions of the company in the context of ESG issues.
    - **Regulatory Risk:** Keep track of changes in relevant regulations and their potential impact on the business.
    """
    return risk_text

def scenario_analysis():
    scenario_text = """
    ## Scenario Analysis
    - **Climate Scenarios:** Simulate how different climate scenarios might affect the company’s operations.
    - **Regulatory Scenarios:** Model the impact of potential regulatory changes on business operations.
    """
    return scenario_text

def investment_analysis():
    investment_text = """
    ## Investment Analysis
    - **ESG Ratings Integration:** Integrate third-party ESG ratings and scores.
    - **Sustainable Investment Opportunities:** Highlight investment opportunities that align with sustainability and ESG criteria.
    - **Impact Metrics:** Measure the impact of investments on sustainability goals.
    """
    return investment_text

def reporting_compliance():
    reporting_text = """
    ## Reporting and Compliance
    - **Automated Reporting:** Generate reports for stakeholders, investors, and regulatory bodies.
    - **Compliance Tracking:** Monitor compliance with relevant ESG regulations and standards.
    """
    return reporting_text

def data_visualization(metric):
    return plot_metrics(metric)

# Gradio Interface
with gr.Blocks() as dashboard:
    with gr.Tabs():
        with gr.TabItem("Overview"):
            gr.Markdown(overview())

        with gr.TabItem("Detailed ESG Analysis"):
            with gr.Accordion("Environmental Metrics"):
                gr.Markdown("""
                ### Environmental Metrics
                **Greenhouse Gas Emissions:** Measures the total emissions of greenhouse gases.
                **Renewable Energy Usage:** Percentage of energy consumption from renewable sources.
                **Water Usage:** Total water consumption and efficiency measures.
                **Pollution Levels:** Levels of pollutants emitted by the company.
                """)
                ghg_emissions = gr.Slider(label="Greenhouse Gas Emissions (in tons)", minimum=0, maximum=1000, step=1)
                renewable_energy = gr.Slider(label="Renewable Energy Usage (%)", minimum=0, maximum=100, step=1)
                water_usage = gr.Slider(label="Water Usage (in cubic meters)", minimum=0, maximum=10000, step=10)
                pollution_levels = gr.Slider(label="Pollution Levels (index)", minimum=0, maximum=100, step=1)
            
            with gr.Accordion("Social Metrics"):
                gr.Markdown("""
                ### Social Metrics
                **Employee Satisfaction:** Overall satisfaction level of employees.
                **Gender and Ethnicity Breakdown:** Diversity metrics of the workforce.
                **Safety Incidents:** Number and severity of workplace safety incidents.
                """)
                employee_satisfaction = gr.Slider(label="Employee Satisfaction (%)", minimum=0, maximum=100, step=1)
                gender_diversity = gr.Slider(label="Gender Diversity (%)", minimum=0, maximum=100, step=1)
                ethnicity_diversity = gr.Slider(label="Ethnicity Diversity (%)", minimum=0, maximum=100, step=1)
                safety_incidents = gr.Slider(label="Safety Incidents (number)", minimum=0, maximum=100, step=1)
            
            with gr.Accordion("Governance Metrics"):
                gr.Markdown("""
                ### Governance Metrics
                **Board Structure:** Composition and diversity of the board.
                **Audit Practices:** Quality and transparency of audit practices.
                **Anti-Corruption Measures:** Policies and measures to prevent corruption.
                **Shareholder Rights:** Measures to protect and enhance shareholder rights.
                """)
                board_structure = gr.Slider(label="Board Structure (index)", minimum=0, maximum=100, step=1)
                audit_practices = gr.Slider(label="Audit Practices (index)", minimum=0, maximum=100, step=1)
                anti_corruption = gr.Slider(label="Anti-Corruption Measures (index)", minimum=0, maximum=100, step=1)
                shareholder_rights = gr.Slider(label="Shareholder Rights (index)", minimum=0, maximum=100, step=1)


        with gr.TabItem("Benchmarking Tools"):
            gr.Markdown(benchmarking_tools())

        with gr.TabItem("Risk Assessment"):
            gr.Markdown(risk_assessment())

        with gr.TabItem("Scenario Analysis"):
            gr.Markdown(scenario_analysis())

        with gr.TabItem("Investment Analysis"):
            gr.Markdown(investment_analysis())

        with gr.TabItem("Reporting and Compliance"):
            gr.Markdown(reporting_compliance())

        with gr.TabItem("Data Visualization"):
            metric = gr.Dropdown(label="Select Metric", choices=list(df.columns[1:]), value='Carbon Footprint')
            plot_button = gr.Button("Plot")
            output_image = gr.Image()
            
            plot_button.click(fn=data_visualization, inputs=metric, outputs=output_image)

dashboard.launch()
