import asyncio
from google.adk.runners import InMemoryRunner

# Import our new Surgeon Agent
try:
    from ai_fixer.agent import root_agent as fixer_agent
except ImportError:
    print("Error: Could not import 'ai_fixer'.")
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
        print("Error: 'diagnosis.txt' not found. Run Step 2 first!")
        return

    print(f"Reading diagnosis...")
    print(f"Targeting file: {BROKEN_FILE_PATH}")

    # 2. Run the Fixer Agent
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