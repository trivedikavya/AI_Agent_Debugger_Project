# 🚀 AI Agent Mechanic: The AI Agent Debugger
A Capstone Project for the 5-Day AI Agents Intensive Course.

**Track:** Freestyle

---

### 1. The Pitch: Problem, Solution, Value

**The Problem (The "Why"):**
AI Agents are powerful, but when they fail, they are a "black box." They produce long, messy, and technical trace logs that are difficult for developers to parse and impossible for non-technical users to understand. This makes debugging slow and frustrating.

**The Solution (The "What"):**
This project is an **"AI Agent Mechanic"**—an AI agent whose sole purpose is to debug *other* agents.

It works in two steps:
1.  A "Broken Agent" (`broken_researcher`) is run, which intentionally fails and produces a messy `broken_agent_trace.log` file.
2.  The "AI Mechanic Agent" (`ai_debugger`) is then run. It reads this log file, analyzes the complex error trace, and produces a simple, plain-English diagnosis of the *root cause* of the failure.

**The Value (The "Impact"):**
This agent turns a 30-minute debugging nightmare into a 3-second diagnosis.
* **For Developers:** Massively speeds up debugging.
* **For Teams:** Allows non-technical product managers to understand *why* an agent failed, improving communication.
* **For the Future:** This "agent-watching-agent" pattern is a key step towards building self-healing agent systems.

---

### 2. The Implementation: Architecture & Code

#### Architecture
This project is a multi-agent system composed of two agents and two scripts:



[Image of a simple architecture diagram]

*(You can create a simple diagram using any free tool and add it here. A simple `[Agent A] -> [Log File] -> [Agent B] -> [Answer]` is perfect.)*

1.  **`broken_researcher` (Agent A):** A simple agent that is *designed to fail*. Its `count_papers` tool requires a `list`, but its instructions trick it into passing a `string`.
2.  **`1_create_error_log.py`:** This script runs Agent A and uses the `LoggingPlugin` (from Day 4a) to capture its full, messy trace log and save it to `broken_agent_trace.log`.
3.  **`ai_debugger` (Agent B):** This is the core of the project. It is an "AI Mechanic" with two custom tools:
    * `read_log_file(path)`: Reads the log file from disk.
    * `find_last_error_in_trace(content)`: Uses Regex to find the *exact* failing tool call in the log.
4.  **`2_run_debugger.py`:** This script runs Agent B and gives it the log file. Agent B uses its tools and LLM brain to provide a simple, one-paragraph diagnosis of the problem.

#### Key Course Concepts Used (Over 3!)
* **[✅] Multi-agent System:** We use two distinct agents (`broken_researcher` and `ai_debugger`) that interact (indirectly) via a log file.
* **[✅] Custom Tools:** The `ai_debugger` is built on two custom-made tools: `read_log_file` and `find_last_error_in_trace`.
* **[✅] Observability (Logging/Tracing):** This entire project is an *application* of observability. We use the `LoggingPlugin` to create a trace and then build a new agent to analyze that trace.
* **[✅] Bonus: Agent Deployment:** The `ai_debugger` agent is packaged for and deployed to **Vertex AI Agent Engine** to earn the deployment bonus point.

---

### 3. How to Run This Project

**Setup:**
1.  Clone this repository.
2.  Install the required libraries: `pip install -r requirements.txt`
3.  Get a Gemini API Key from **Google AI Studio**.
4.  Paste your API key into *both* of these files:
    * `broken_researcher/.env`
    * `ai_debugger/.env`

**Demo:**
To run the full demo, just run the two main scripts in order:

**Step 1: Create the error log**
```bash
python 1_create_error_log.py
python 2_run_debugger.py
```