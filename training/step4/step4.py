from google.adk.agents import LlmAgent
from .tools import marketing_tool

# Create the agent
root_agent = LlmAgent(
    name="marketing_data_agent",
    model="gemini-2.0-flash",
    description="An agent that analyzes marketing campaign data from CSV files",
    instruction="""You are a helpful marketing data analyst. When users ask about marketing data, 
    campaign performance, or want insights from the data, use the analyze_marketing_data tool. 
    Provide clear, helpful explanations of the data insights.""",
    tools=[marketing_tool]
)






