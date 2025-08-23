from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)

# Custom imports
from Jarvis_prompts import behavior_prompts, Reply_prompts
from Jarvis_google_search import google_search, get_current_datetime
from jarvis_get_whether import get_weather
from Jarvis_window_CTRL import open, close, folder_file
from Jarvis_file_opner import Play_file
from keyboard_mouse_CTRL import (
    move_cursor_tool, mouse_click_tool, scroll_cursor_tool,
    type_text_tool, press_key_tool, swipe_gesture_tool,
    press_hotkey_tool, control_volume_tool
)

# ✅ HARDCODED API KEYS AND CONFIG
GOOGLE_API_KEY = "AIzaSyB5VHIZUMcGakCgUi-YVKYlygUDJ1CW6X8"
LIVEKIT_API_KEY = "APIoMspNSSH8Vj6"
LIVEKIT_API_SECRET = "Rual5GuslAc96f1txZMyE0AME24wtu0h1pJ6BrBm3rV"
LIVEKIT_URL = "wss://jarvis-i91cwuzo.livekit.cloud"
GOOGLE_SEARCH_API_KEY = "AIzaSyCrPlZ6KNSSYCMDSMNWreBfjzY2EwtCo24"
SEARCH_ENGINE_ID = "e0f1f50a215614e3c"

# Define the Assistant agent with tools
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=behavior_prompts,
            tools=[
                google_search,
                get_current_datetime,
                get_weather,
                open,
                close,
                folder_file,
                Play_file,
                move_cursor_tool,
                mouse_click_tool,
                scroll_cursor_tool,
                type_text_tool,
                press_key_tool,
                press_hotkey_tool,
                control_volume_tool,
                swipe_gesture_tool
            ]
        )

# Entry point to start agent
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="Charon",
            api_key=GOOGLE_API_KEY
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
            video_enabled=True
        ),
    )

    await ctx.connect()
    await session.generate_reply(instructions=Reply_prompts)

# Run as app
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
