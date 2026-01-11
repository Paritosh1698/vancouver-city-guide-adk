import os

from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

DATASTORE_ID = "projects/adk-agent-481717/locations/global/collections/default_collection/dataStores/vancouver-neighbourhoods_1767224800692"

neighbourhood_info = Agent(
    name="neighbourhood_info",
    model="gemini-3-pro-preview",
    description="Agent that returns information, history and wikipedia url about neighbourhoods in Vancouver.",
    instruction="""
        You're an agent that provides key details, historical facts and wikipedia links about different neighbourhoods.

        When asked about a particular neighbourhood:
        1. Use the tool to look for the specific neighbourhood.
        2. Ask the user if they want to know about the history of the neighbourhood.
        3. If the user responds with affirmation, provide the history and the wikipedia url.

        Start the response in the following format:
        "Here's the wikipedia article about the neighbourhood" and add the wikipedia url:"

        If the user asks about anything else, 
        you should delegate the task to the vancouver city guide agent.
        """,
    tools=[VertexAiSearchTool(data_store_id=DATASTORE_ID)],
)