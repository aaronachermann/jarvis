# 🧠 Jarvis – Local Voice-Controlled AI Assistant

**Jarvis** is a voice-activated, conversational AI assistant powered by a local LLM via Ollama. It listens for any sentence containing its name, processes spoken commands using LangChain and responds out loud via TTS. Tools are loaded dynamically and can be switched on or off in `config.py`.

---

## 🚀 Features

- 🗣 Voice-activated with wake word **"Jarvis"**
- 🧠 Local language model (Llama3.2 via Ollama)
- 🔧 Tool-calling with LangChain
- 🛠 Tools are loaded dynamically from the `tools` folder and controlled via `config.py`
- 🔌 Plugins are discovered automatically at startup
- 💾 Conversation memory plugin (can be disabled)
- 📆 Calendar and Apple Calendar plugins plus social, vision and learning modules
- 🔊 Text-to-speech responses via `pyttsx3`
- 🌍 Example tool: Get the current time in a given city
- ⛅ Weather reports, web search and more tools
- 📍 Enhanced context with location and device activity
- 🔎 Semantic memory search and pattern-based suggestions
- 🏠 Home automation hooks for smart devices
- 🌐 Research assistant for crawling web pages
- 📂 Read-only access to local files
- 🖥 Web dashboard to toggle plugins at runtime
- 🔐 Optional support for OpenAI API integration

---


## ▶️ How It Works (`main.py`)

1. **Startup & local LLM Setup**
   - Initializes a local Ollama model (`llama3.2:1b`) via `ChatOllama`
   - Loads all enabled tools from the `tools` package automatically

2. **Wake Word Listening**
   - Listens via microphone (e.g., `device_index=0`)
   - If it hears the word **"Jarvis"**, it enters "conversation mode"

3. **Voice Command Handling**
   - Records the user’s spoken command
   - Passes the command to the LLM, which may invoke tools
   - Responds using `pyttsx3` text-to-speech (with optional custom voice)
   - Conversation history can be exported to `conversation_export.txt`

4. **Timeout**
   - If the user is inactive for more than 30 seconds in conversation mode, it resets to wait for the wake word again.

---

## 🤖 How To Start Jarvis

1. **Install Dependencies**  
   Make sure you have installed all required dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up the Local Model**
   Ensure you have the `llama3.2:1b` model available in Ollama.

3. **Run Jarvis**
   Start the assistant by running:
   ```bash
   python main.py
   ```
   You can enable or disable features by editing `config.py`.
   Apple Calendar integration requires macOS with EventKit permissions.
4. **Plugin Dashboard**
   Launch the optional web dashboard with:
   ```bash
   python dashboard.py
   ```
---

