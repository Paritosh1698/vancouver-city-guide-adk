from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from vancouver_city_guide.profanity_guard import profanity_before_model_callback
from vancouver_city_guide.sub_agents.location_lookup.agent import location_lookup
from vancouver_city_guide.sub_agents.neighbourhood_info.agent import neighbourhood_info

root_agent = LlmAgent(
    name = "vancouver_city_guide",
    model = "gemini-3-pro-preview",
    description = "Agent that provides a visitor with useful information about the city of Vancouver, British Columbia, Canada.",
    instruction = """
    You're the Vancouver city guide.
        
    Greet the user and ask them about their location in the city, specifically the street and street number.
        
    Goal: help users explore Vancouver with accurate, tool-grounded answers.
        
    When needed, delegate to the following agents:
    - Use sub agent `location_lookup` to geocode a place/address.
    - Use the tool `neighbourhood_info` to provide history and wikipedia link of a Vancouver neighbourhood.
        
    Follow this response format:
    - Return a concise answer, then a short 'Details' section with any useful links.
    - If a tool fails, explain what went wrong and suggest a next best step.
    """,
    sub_agents = [location_lookup],
    tools = [AgentTool(neighbourhood_info)],
    before_model_callback = profanity_before_model_callback
    )