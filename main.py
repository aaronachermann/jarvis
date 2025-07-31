import os
import logging
import time
import pyttsx3
import threading
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

load_dotenv()

MIC_INDEX = 2
TRIGGER_WORD = "jarvis"
CONVERSATION_TIMEOUT = 30  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.DEBUG) # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

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
def speak_text(text: str) -> None:
    """Speak text asynchronously so printing continues."""
    def _run():
        try:
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

    threading.Thread(target=_run, daemon=True).start()

# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None
    conversation_log = []

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio, language="it-IT")
                        logging.info(f"Heard: {transcript}")
                        print(f"Tu: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"Triggered by: {transcript}")
                            speak_text("Sì, signore?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("Timeout: Returning to wake word mode.")
                            conversation_mode = False
                            continue
                        logging.info("Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio, language="it-IT")
                        logging.info(f"Command: {command}")
                        print(f"Tu: {command}")

                        logging.info("Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        logging.info(f"Agent responded: {content}")

                        print("Jarvis:", content, flush=True)
                        speak_text(content)
                        if FEATURE_FLAGS.get("memory"):
                            memory.store(command, content)
                        if FEATURE_FLAGS.get("learning_module"):
                            learning.record("command")
                        if FEATURE_FLAGS.get("conversation_history"):
                            conversation_log.append((command, content))
                        last_interaction_time = time.time()

                except sr.WaitTimeoutError:
                    logging.warning("Timeout waiting for audio.")
                    if conversation_mode and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                        logging.info("No input in conversation mode. Returning to wake word mode.")
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("Could not understand audio.")
                except Exception as e:
                    logging.error(f"Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"Critical error in main loop: {e}")
    finally:
        if FEATURE_FLAGS.get("conversation_history"):
            try:
                with open("conversation_export.txt", "w", encoding="utf-8") as f:
                    for usr, ans in conversation_log:
                        f.write(f"U: {usr}\nA: {ans}\n")
            except Exception as e:
                logging.error(f"Failed to export conversation: {e}")

if __name__ == "__main__":
    write()
