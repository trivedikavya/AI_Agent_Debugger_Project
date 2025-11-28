import asyncio
import logging
import os
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin

# This script can fail if the agent isn't found, so we'll import it safely
try:
    from broken_researcher.agent import root_agent as broken_agent
except ImportError:
    print("Error: Could not import 'broken_researcher'.")
    print("Please make sure the 'broken_researcher' folder and 'agent.py' exist.")
    exit()

# This is the "ugly" log file we are going to create
LOG_FILE_NAME = "broken_agent_trace.log"

print(f"--- Starting 'broken_researcher' to create a log file ---")

# --- Setup the Logger to save the trace to a file ---
# We set level=logging.INFO to capture all the plugin's trace messages
logging.basicConfig(
    filename=LOG_FILE_NAME,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True  # This overwrites the old log file every time you run it
)

# This is the main function to run our agent
async def run_broken_agent():
    print(f"Attempting to run the broken agent...")
    print(f"All trace output will be saved to: {LOG_FILE_NAME}")

    # Create a runner and add the LoggingPlugin (from Day 4a)
    runner = InMemoryRunner(
        agent=broken_agent,
        plugins=[LoggingPlugin()]  # This plugin writes the trace to our logger
    )

    # We will run the agent with a prompt that we know will make it fail
    try:
        response = await runner.run_debug(
            "Find papers on 'quantum computing', get a summary, and count the summary."
        )
        print("\nAgent finished... but it might not have failed as expected.")
    except Exception as e:
        # We EXPECT it to fail. This is good!
        print(f"\nAgent failed as expected! The error was: {e}")

    print(f"\n✅ Success! The 'ugly' log file '{LOG_FILE_NAME}' has been created.")
    print("You can now run '2_run_debugger.py' to analyze this file.")

# This is how we run the main function
if __name__ == "__main__":
    asyncio.run(run_broken_agent())