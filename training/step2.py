from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="coordinator_agent",
    model="gemini-2.0-flash",
    description="An agent that can answer basic questions and delegate tasks to other agents",
    instruction="""
    You are a coordinator agent that talks with the user and answer it's questions
    If the user asks you to search something on Google use the search_agent tool""",
    tools=[google_search],
)






