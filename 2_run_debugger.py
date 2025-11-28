import asyncio
from google.adk.runners import InMemoryRunner

# We wrap the import in a try/except block to give a helpful error message
# if the folder setup isn't correct yet.
try:
    from ai_debugger.agent import root_agent as debugger_agent
except ImportError:
    print("Error: Could not import 'ai_debugger'.")
    print("Please make sure the 'ai_debugger' folder and 'agent.py' exist.")
    exit()

# Configuration
LOG_FILE_TO_DEBUG = "broken_agent_trace.log" # Input: The messy log file
DIAGNOSIS_FILE = "diagnosis.txt"             # Output: The file for the Fixer Agent

async def run_debugger():
    print(f"--- Starting 'AI Debugger Agent' ---")
    print(f"Analyzing the log file: {LOG_FILE_TO_DEBUG}...")

    # Initialize the runner with our Debugger Agent
    runner = InMemoryRunner(agent=debugger_agent)

    # We give the agent the *path* to the log file as its prompt.
    # The agent uses its tools to read the file and find the error.
    response_trace = await runner.run_debug(
        f"Please analyze the agent log file located at: {LOG_FILE_TO_DEBUG}"
    )

    print("\n--- AI Debugger's Final Report ---")

    # The 'response_trace' is a list of all events (tools calls, thoughts, etc.)
    # The final, plain-English answer is the last text part from the last event.
    try:
        if response_trace:
            # Extract the final text explanation
            final_diagnosis = response_trace[-1].content.parts[0].text
            
            # Print it to the console for you to see
            print(final_diagnosis)

            # --- CRITICAL STEP FOR THE FIXER AGENT ---
            # We save this diagnosis to a file so the 'ai_fixer' agent can read it later.
            print(f"\nSaving diagnosis to '{DIAGNOSIS_FILE}'...")
            with open(DIAGNOSIS_FILE, "w") as f:
                f.write(final_diagnosis)
            
            print(f"✅ Diagnosis saved! You can now run '3_run_fixer.py'.")
            
        else:
            print("The agent did not return a final response.")

    except Exception as e:
        print(f"Could not get final response from agent trace. Error: {e}")
        # If debugging this script, you can uncomment the next line to see the raw data:
        # print("Here is the raw trace:", response_trace)

# This is the standard boilerplate to run async Python scripts
if __name__ == "__main__":
    asyncio.run(run_debugger())