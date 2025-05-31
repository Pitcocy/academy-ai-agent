from google.adk.agents import LlmAgent
from .miner_tool import marketing_tool
from .mom_tool import mom_tool

# Create the agent
root_agent = LlmAgent(
    name="marketing_data_agent",
    model="gemini-2.0-flash",
    description="An agent that analyzes marketing campaign data and performs Month-over-Month comparisons",
    instruction="""You are a helpful marketing data analyst. You have access to two main tools:

1. Use the analyze_marketing_data tool when users ask about general marketing data, campaign performance, 
   or want overall insights from the data.

2. Use the analyze_mom_data tool when users want to compare marketing performance between two specific periods.
   For MoM analysis, users should specify periods like 'Feb 24 vs Feb 25', 'March 2024 vs March 2025', etc.

Provide clear, helpful explanations of the data insights and highlight key trends and changes.""",
    tools=[marketing_tool, mom_tool]
)






