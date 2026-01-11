import re
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types

BANNED_WORDS = {
    "fuck", "shit", "bitch", "asshole", "bastard", "cunt", "retard", "nig"
    }

_WORD_RE = re.compile(r"[a-zA-Z]+")

def _contains_profanity(text: str) -> bool:
    tokens = [t.lower() for t in _WORD_RE.findall(text or "")]
    return any(t in BANNED_WORDS for t in tokens)

def profanity_before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    last_user_message = ""
    if llm_request.contents and len(llm_request.contents) > 0:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts and len(content.parts) > 0:
                if hasattr(content.parts[0], "text") and content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    if _contains_profanity(last_user_message):
        # Profanity counter used for evaluation in later stages
        callback_context.state["profanity_hits"] = (callback_context.state.get("profanity_hits", 0) or 0) + 1

        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text=(
                            "I can’t help with messages that contain inappropriate language. "
                            "Please rephrase, and I’ll help you with city info."
                        )
                    )
                ],
            )
        )

    return None
