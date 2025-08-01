# 🧠 Jarvis – Local Voice-Controlled AI Assistant

**Jarvis** is a conversational AI assistant powered by a local LLM via Ollama. You type commands directly in the terminal and Jarvis responds out loud via TTS. Tools are loaded dynamically and can be switched on or off in `config.py`.


---

## 🚀 Features

- ⌨️ Command-line interface: type your prompts

- 🧠 Local language model (Llama3.2 via Ollama)
- 🔧 Tool-calling with LangChain
- 🛠 Tools are loaded dynamically from the `tools` folder and controlled via `config.py`
- 🔌 Plugins are discovered automatically at startup
- 💾 Conversation memory plugin (can be disabled)
- 📆 Calendar and Apple Calendar plugins plus social, vision and learning modules
- 🔊 Text-to-speech responses via `pyttsx3`
- 🎞 Animated concentric-ring HUD using `curses` while Jarvis speaks
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

2. **Command Input**
   - Type a command and press **Enter**
   - The assistant sends the text to the LLM and may invoke tools
   - Responses are spoken using `pyttsx3` while the HUD animates
   - Conversation history is saved to `conversation_export.txt` on exit


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

