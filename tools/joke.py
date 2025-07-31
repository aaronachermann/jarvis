from langchain.tools import tool
import random

_JOKES = [
    "Perche' il computer e' andato dal dottore? Aveva un virus!",
    "Qual e' il colmo per un programmatore? Avere troppi bug e pochi snack.",
    "Perche' gli sviluppatori amano il buio? Perche' la luce attira gli insetti.",
]

@tool
def tell_joke(_: str = "") -> str:
    """Racconta una barzelletta a caso."""
    return random.choice(_JOKES)
