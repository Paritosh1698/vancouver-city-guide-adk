import asyncio

from google import adk
from google.adk.sessions import VertexAiSessionService
from google.genai import types

from vancouver_city_guide.agent import root_agent

APP_NAME = "vancouver-city-guide"
PROJECT = "adk-agent-481717"
LOCATION = "us-central1"
AGENT_ENGINE_ID = "3404480525245612032"

async def main():
    user_id = "Paritosh",
    session_id = "demo-session-1",

    session_service = VertexAiSessionService(
        project = PROJECT,
        location = LOCATION,
        agent_engine_id = AGENT_ENGINE_ID,
    )

    existing_sessions = await session_service.list_sessions(
        app_name = APP_NAME,
        user_id = user_id,
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:
        session_id = existing_sessions.sessions[0].id
    else:
        new_session = await session_service.create_session(
            app_name = APP_NAME,
            user_id = user_id,
        )
        session_id = new_session.id

    runner = adk.Runner(
        agent = root_agent,
        session_service = session_service,
        app_name = APP_NAME,
    )

    while True:
        user_input = input("")

        if user_input.lower() in ["exit", "quit"]:
            break

        msg = types.Content(role="user", parts=[types.Part(text=user_input)])

        async for event in runner.run_async(
                user_id = user_id,
                session_id = session_id,
                new_message = msg,
        ):
            if event.is_final_response():
                print(event.content.parts[0].user_input)

if __name__ == "__main__":
    asyncio.run(main())

