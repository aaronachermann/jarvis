import os
import logging
import pyttsx3
import threading
import curses
from dotenv import load_dotenv


from dotenv import load_dotenv
import speech_recognition as sr

from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import load_tools
from config import ENABLED_TOOLS, FEATURE_FLAGS
from plugins import setup_plugins
from plugins.memory import memory
from plugins.learning import learning
from hud import RingHUD

load_dotenv()

logging.basicConfig(level=logging.DEBUG)  # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

# Initialize LLM
# llm = ChatOllama(model="qwen3:1.7b", reasoning=False)

# model that supports italian and is available on ollama
llm = ChatOllama(model="llama3.2:1b", reasoning=False)

# llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, organization=org_id) for openai

# Load all available tools dynamically based on configuration
tools = load_tools()

# Tool-calling prompt
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}")
# ])

# italian version of the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu sei Jarvis, un assistente AI intelligente e conversazionale. Il tuo obiettivo è essere utile, amichevole e informativo. Puoi rispondere con un linguaggio naturale, simile a quello umano, e utilizzare strumenti quando necessario per rispondere alle domande in modo più accurato. Spiega sempre il tuo ragionamento in modo semplice quando è il caso e mantieni le tue risposte colloquiali e concise."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Initialise plugins
setup_plugins()

# TTS setup
def speak_text(text: str, hud: RingHUD) -> None:
    """Speak text asynchronously while showing HUD animation."""

    def _run() -> None:
        try:
            hud.start_animation()
            engine = pyttsx3.init()
            for voice in engine.getProperty('voices'):
                name = voice.name.lower()
                if "brittany" in name or "en-gb" in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS failed: {e}")
        finally:
            hud.stop_animation()

    threading.Thread(target=_run, daemon=True).start()

def chat(stdscr: curses.window, hud: RingHUD) -> None:
    """Read typed commands and respond using the LLM."""
    conversation_log: list[tuple[str, str]] = []
    curses.echo()
    height, width = stdscr.getmaxyx()
    input_y = height - 1

    while True:
        try:
            stdscr.move(input_y, 0)
            stdscr.clrtoeol()
            stdscr.addstr(input_y, 0, "> ")
            stdscr.refresh()
            user_bytes = stdscr.getstr(input_y, 2)
            if not user_bytes:
                continue
            command = user_bytes.decode().strip()
        except KeyboardInterrupt:
            break

        if command.lower() in {"exit", "quit"}:
            break

        hud.log(f"Tu: {command}")
        try:
            response = executor.invoke({"input": command})
            content = response["output"]
        except Exception as e:  # fallback on error
            content = f"Errore: {e}"
        hud.log(f"Jarvis: {content}")
        speak_text(content, hud)
        if FEATURE_FLAGS.get("memory"):
            memory.store(command, content)
        if FEATURE_FLAGS.get("learning_module"):
            learning.record("command")
        if FEATURE_FLAGS.get("conversation_history"):
            conversation_log.append((command, content))

    if FEATURE_FLAGS.get("conversation_history"):
        try:
            with open("conversation_export.txt", "w", encoding="utf-8") as f:
                for usr, ans in conversation_log:
                    f.write(f"U: {usr}\nA: {ans}\n")
        except Exception as e:
            logging.error(f"Failed to export conversation: {e}")


def _curses_main(stdscr: curses.window) -> None:
    hud = RingHUD(stdscr)
    hud.start()
    chat(stdscr, hud)
    hud.running = False
    hud.join()



if __name__ == "__main__":
    curses.wrapper(_curses_main)
