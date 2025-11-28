import asyncio
import os
from dotenv import load_dotenv # <--- IMPORTANT IMPORT
from google.adk.runners import InMemoryRunner

# <--- IMPORTANT: Load the API Key immediately --->
load_dotenv()

# Check if the key exists (Safe check)
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERROR: GOOGLE_API_KEY not found!")
    print("Make sure you have a .env file in the main folder.")
    exit()

# Import our Surgeon Agent
try:
    from ai_fixer.agent import root_agent as fixer_agent
except ImportError:
    print("Error: Could not import 'ai_fixer'.")
    print("Check if the folder exists.")
    exit()

# Configuration
BROKEN_FILE_PATH = "broken_researcher/agent.py"
DIAGNOSIS_FILE = "diagnosis.txt"

async def run_fixer():
    print(f"--- Starting 'AI Fixer Agent' ---")
    
    # 1. Read the diagnosis from the previous step
    try:
        with open(DIAGNOSIS_FILE, "r") as f:
            diagnosis_content = f.read()
    except FileNotFoundError:
        print("Error: 'diagnosis.txt' not found. Run '2_run_debugger.py' first!")
        return

    print(f"Reading diagnosis...")
    print(f"Targeting file: {BROKEN_FILE_PATH}")

    # 2. Initialize the runner (Now it has the API Key!)
    runner = InMemoryRunner(agent=fixer_agent)
    
    # We give the agent the Context (Diagnosis) and the Target (File Path)
    await runner.run_debug(
        f"""
        Please fix the code in this file: '{BROKEN_FILE_PATH}'
        
        Here is the diagnosis of the error:
        "{diagnosis_content}"
        
        Read the file, fix the logic error, and overwrite the file with the working code.
        """
    )
    
    print("\n✅ Fix attempt complete. Check 'broken_researcher/agent.py' to see the changes!")

if __name__ == "__main__":
    asyncio.run(run_fixer())