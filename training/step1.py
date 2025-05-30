from google.adk.agents import LlmAgent


root_agent = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="An agent that can answer basic questions and delegate tasks to other agents",
    tools=[],
)







