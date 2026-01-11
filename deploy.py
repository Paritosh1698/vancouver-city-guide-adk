import vertexai
from vertexai import agent_engines
from vancouver_city_guide.agent import root_agent

# CONFIGURATION
PROJECT_ID = "adk-agent-481717"
REGION = "us-central1"
STAGING_BUCKET = "gs://adk-agent-481717-adk-staging"

vertexai.init(project=PROJECT_ID, location=REGION, staging_bucket=STAGING_BUCKET)

# 1. Define the requirements exactly
requirements = [
    "google-adk>=1.15.1",
    "google-genai",
    "google-cloud-aiplatform[adk,agent_engines]>=1.112.0",
    "requests",
    "python-dotenv",
    ]

# 2. Package your local code
# This tells Vertex AI to include these folders in the remote container's PYTHONPATH
extra_packages = [
    "./vancouver_city_guide",  # Your main folder
]

print("Starting deployment to Agent Engine...")

try:
    # We wrap the ADK agent in an AdkApp for the Reasoning Engine
    from vertexai.preview import reasoning_engines

    adk_app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    # Create the remote resource
    remote_app = agent_engines.create(
        agent_engine=adk_app,
        requirements=requirements,
        extra_packages=extra_packages,
        display_name="Vancouver City Guide - ADK"
    )

    print(f"Deployment successful! Resource ID: {remote_app.resource_name}")

except Exception as e:
    print(f"Deployment failed with error: {e}")