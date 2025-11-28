import asyncio
from google.adk.runners import InMemoryRunner

# This script can fail if the agent isn't found
try:
    from ai_debugger.agent import root_agent as debugger_agent
except ImportError:
    print("Error: Could not import 'ai_debugger'.")
    print("Please make sure the 'ai_debugger' folder and 'agent.py' exist.")
    exit()

# This is the "ugly" log file we created in the first script
LOG_FILE_TO_DEBUG = "broken_agent_trace.log"

# This is the main function to run our debugger
async def run_debugger():
    print(f"--- Starting 'AI Debugger Agent' ---")
    print(f"Analyzing the log file: {LOG_FILE_TO_DEBUG}...")

    runner = InMemoryRunner(agent=debugger_agent)

    # We give the agent the *path* to the log file as its prompt
    response_trace = await runner.run_debug(
        f"Please analyze the agent log file located at: {LOG_FILE_TO_DEBUG}"
    )

    print("\n--- AI Debugger's Final Report ---")

    # The 'response_trace' is a list of all events.
    # The final, plain-English answer is the last text part from the last event.
    try:
        if response_trace:
            final_text = response_trace[-1].content.parts[0].text
            print(final_text)
        else:
            print("The agent did not return a final response.")
    except Exception as e:
        print(f"Could not get final response from agent trace. Error: {e}")
        print("Here is the raw trace:", response_trace)

# This is how we run the main function
if __name__ == "__main__":
    asyncio.run(run_debugger())