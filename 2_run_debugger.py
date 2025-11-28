import asyncio
import os
from dotenv import load_dotenv # <--- NEW IMPORT
from google.adk.runners import InMemoryRunner

# <--- NEW: Force load the .env file immediately --->
load_dotenv() 

# Check if the key was loaded (for debugging)
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERROR: GOOGLE_API_KEY not found in environment variables!")
    print("Please make sure you have a .env file in this folder with your key.")
    exit()

try:
    from ai_debugger.agent import root_agent as debugger_agent
except ImportError:
    print("Error: Could not import 'ai_debugger'.")
    exit()

# Configuration
LOG_FILE_TO_DEBUG = "broken_agent_trace.log"
DIAGNOSIS_FILE = "diagnosis.txt"

async def run_debugger():
    print(f"--- Starting 'AI Debugger Agent' ---")
    print(f"Analyzing the log file: {LOG_FILE_TO_DEBUG}...")

    # Initialize the runner (It will now find the key in the environment!)
    runner = InMemoryRunner(agent=debugger_agent)

    response_trace = await runner.run_debug(
        f"Please analyze the agent log file located at: {LOG_FILE_TO_DEBUG}"
    )

    print("\n--- AI Debugger's Final Report ---")

    try:
        if response_trace:
            final_diagnosis = response_trace[-1].content.parts[0].text
            print(final_diagnosis)

            print(f"\nSaving diagnosis to '{DIAGNOSIS_FILE}'...")
            with open(DIAGNOSIS_FILE, "w") as f:
                f.write(final_diagnosis)
            print(f"✅ Diagnosis saved! You can now run '3_run_fixer.py'.")
        else:
            print("The agent did not return a final response.")

    except Exception as e:
        print(f"Could not get final response. Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_debugger())