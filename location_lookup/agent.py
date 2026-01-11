import os
import requests

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from typing import Dict, Any

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def get_location(street: str, street_number: str) -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"ok": False, "error": "Missing GOOGLE_MAPS_API_KEY", "street": street, "street_number": street_number}

    address = f"{street_number} {street}, Vancouver, BC, Canada"

    try:
        r = requests.get(
            GOOGLE_GEOCODE_URL,
            params={"address": address, "key": api_key},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()

        if data.get("status") != "OK" or not data.get("results"):
            return {"ok": False, "error": f"Geocoding failed: {data.get('status')}", "address": address}

        top = data["results"][0]
        loc = top["geometry"]["location"]
        return {
            "ok": True,
            "address": address,
            "formatted_address": top.get("formatted_address"),
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
            "place_id": top.get("place_id"),
            "types": top.get("types", []),
        }

    except requests.RequestException as e:
        return {"ok": False, "error": str(e), "address": address}

def _norm(s: str) -> str:
    return (s or "").strip().lower()

def check_address(street: str, street_number: str, tool_context: ToolContext) -> Dict[str, Any]:
    prev_street = tool_context.state.get("street")
    prev_st_number = tool_context.state.get("street_number")

    is_same = (_norm(prev_street) == _norm(street)) and (_norm(prev_st_number) == _norm(street_number))

    tool_context.state["street"] = street
    tool_context.state["street_number"] = street_number
    tool_context.state["address_key"] = f"{_norm(street_number)}|{_norm(street)}"

    return {
        "previous": {"street": prev_street, "street_number": prev_st_number},
        "current": {"street": street, "street_number": street_number},
        "is_same_as_previous": is_same,
    }

location_lookup = Agent(
    name="location_lookup",
    model="gemini-3-pro-preview",
    description="Agent that finds the neighbourhood of an address in Vancouver, British Columbia, Canada.",
    instruction="""
        You're an agent that assists in finding the neighbourhood of an address in Vancouver.
        
        When asked about a particular address:
        1. Call the check_address tool (street and street number).
        2. If 'is_same_as_previous' is true:
            - Tell the user they already provided that address.
            - Ask the user if they want to geocode it anyway (refresh) or move to neighbourhood/history.
            - Only call 'get_location' only if the user explicitly wants to refresh it.
        3. if 'is_same_as_previous' is false:
            - Call the 'get_location(street, street number).
        
        After calling the get_location:
        1. If the location is in Vancouver, inform the user of the neighbourhood they are in.
        2. If the location is not in Vancouver, ask for the street address in Vancouver, British Columbia, Canada.
        
        Start the response in the following format:
        "Here's the neighbourhood you are currently in:"
        
        Ask the user if they want to know about the history of the neighbourhood they are currently in:
        1. If the user says yes, delegate the flow to the neighbourhood info agent.
        2. If the user says no, pass the control to the vancouver city guide agent
    
        If the user asks about anything else, 
        you should delegate the task to the vancouver city guide agent.
        """,
    tools = [get_location, check_address],
)