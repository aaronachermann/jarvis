# Global configuration for Jarvis features and tools.

# Enable or disable individual tools by name. The name must match the
# module file in the ``tools`` package (without ``.py`` extension).
ENABLED_TOOLS = {
    "time": True,
    "weather": True,
    "web_search": True,
    "joke": True,
    "memory_tools": True,
    "calendar_tools": True,
    "social_tools": True,
    "vision_tools": True,
    "learning_tools": True,
    "context_tools": True,
    "apple_calendar_tools": True,
    "home_automation_tools": True,
    "research_tools": True,
    "file_access_tools": True,
}

# General features that are not tools. These flags can be used by
# plugins or the main application to quickly enable/disable
# functionality.
FEATURE_FLAGS = {
    "voice_interface": True,
    "conversation_history": True,
    "memory": True,
    "calendar": True,
    "learning_module": True,
    "context_engine": True,
    "research_assistant": True,
    "home_automation": True,
    "file_access": True,
    "social_manager": True,
    "vision_analysis": True,
    "apple_calendar": True,
}
