from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="coordinator_agent",
    model="gemini-2.0-flash",
    description="A Google Search Agent",
    instruction="""
    You are a Google Search Agent that can search the web for information.
    You can use the google_search tool to search the web.""",
    tools=[google_search]
)






