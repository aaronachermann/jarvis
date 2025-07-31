"""Vision analysis tools."""
from langchain.tools import tool
from plugins.vision import vision

@tool
def capture(_: str = "") -> str:
    """Capture an image using the camera if available."""
    return vision.capture()
