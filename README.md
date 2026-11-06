Haklısın, iç içe geçen kod blokları yüzünden arayüz Markdown formatını bozmuş.

Aşağıdaki tek bir kod kutusunun sağ üstündeki **Kopyala (Copy)** butonuna basarak `README.md` dosyanın içine doğrudan yapıştırabilirsin:

```markdown
# 🤖 Jarvis - Offline Local AI Desktop Assistant

Jarvis is a fully offline, voice- and text-controlled Python desktop AI assistant capable of automating system-level tasks and reading/editing code in a secure sandbox environment.

It operates entirely locally on your hardware without relying on cloud APIs (OpenAI, Anthropic, etc.) or internet connectivity, guaranteeing privacy, low latency, and high performance.

---

## ✨ Key Features

* **🎙️ Hybrid Input System:**
  * **Voice Mode:** Hold the `Right CTRL` key to speak (Push-to-Talk).
  * **Text Mode:** Press the `TAB` key to type directly into the terminal.
* **🧠 Local LLM & Tool Calling (Function Calling):**
  * Powered by **Ollama & Qwen 7B** for logical decision-making.
  * Automatically triggers system tools (playing music via YouTube, opening applications, reading/writing files) based on user intent.
* **🔒 Sandbox Security Architecture (Path Traversal Protection):**
  * File read/write permissions are strictly bounded to the project directory using `os.path.commonpath` checks, preventing access to critical system files.
* **⚡ Non-Blocking Speech & Interruption (TTS):**
  * The `pyttsx3` speech engine runs inside an isolated `multiprocessing` process.
  * Press `ESC` at any time to instantly interrupt long speech outputs.
* **💾 Persistent Memory & Context Truncation:**
  * Conversation history is logged in a **SQLite** database.
  * To maximize speed on GPUs with lower VRAM, only a dynamic window of the last 6 messages is injected into Ollama context.
* **🎯 Dynamic Temperature:**
  * Uses `0.1` temperature for coding, debugging, and file operations to ensure logical accuracy, and `0.3` for standard conversation.

---

## 🛠️ Architecture & Stack

| Component | Technology / Library | Description |
| :--- | :--- | :--- |
| **LLM Engine** | Ollama (Qwen 7B) | Local natural language processing & tool execution |
| **STT (Speech-to-Text)** | Faster-Whisper | Fast & accurate speech recognition with minimal resource usage |
| **TTS (Text-to-Speech)** | Pyttsx3 + Multiprocessing | Interruptible, non-blocking local text-to-speech engine |
| **Memory** | SQLite3 | Local database for conversation logging |
| **Control & Input** | Keyboard & OS Standard Libs | Hardware-level keystroke handling & system command execution |

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.10** or higher
* **Ollama** installed and running on your system

Pull the default model via terminal:
```bash
ollama pull qwen2.5:7b
```

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/your-username/jarvis-assistant.git](https://github.com/your-username/jarvis-assistant.git)
cd jarvis-assistant
pip install -r requirements.txt
```

### 3. Running Jarvis
Run `main.py` (Administrator privileges are recommended for the `keyboard` module to capture global hotkeys):
```bash
python main.py
```

---

## 🎮 How to Use

* **Voice Input:** Press and hold **`Right CTRL`**, speak your command, and release the key.
* **Text Input:** Press **`TAB`**. Once the prompt appears, type your message and press **Enter**.
* **Interrupt Speech:** Press **`ESC`** while Jarvis is speaking to instantly stop audio playback.
* **Shutdown:** Say or type *"exit"*, *"quit"*, *"stop"*, or *"goodbye"*.

---

## 📂 Project Structure

```text
├── main.py          # Core event loop, hybrid input handling & tool execution
├── voice.py         # Multiprocessing-based, ESC-interruptible TTS module
├── ear.py           # Faster-Whisper Push-to-Talk audio recognition module
├── memory.py        # SQLite database logger & context window manager
├── tools.py         # Sandboxed file I/O, app launcher & YouTube integration
├── jarvis_memory.db # Auto-generated local database (Git ignored)
└── README.md        # Project documentation
```

---

## 🛡️ Security & Privacy

Jarvis runs tools capable of interacting with your operating system. Safety measures include:
1. `tools.py` uses `_is_safe_path()` verification to block directory traversal (`../`) attacks outside the workspace.
2. All voice processing, text generation, and conversation logging are kept 100% local.

---

## 👤 Author

* **Arda Muhammed Çakır** - Computer Engineering Student

```