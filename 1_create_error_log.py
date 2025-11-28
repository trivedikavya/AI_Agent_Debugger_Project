import asyncio
import logging
import os
from dotenv import load_dotenv # <--- ADD THIS
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin

# <--- ADD THIS: Load the key so the agent can actually run ---
load_dotenv()

try:
    from broken_researcher.agent import root_agent as broken_agent
except ImportError:
    print("Error: Could not import 'broken_researcher'.")
    exit()

LOG_FILE_NAME = "broken_agent_trace.log"

# Setup the Logger
logging.basicConfig(
    filename=LOG_FILE_NAME,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True 
)

async def run_broken_agent():
    print(f"--- Starting 'broken_researcher' to create a log file ---")
    
    # Check for key before starting
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: API Key missing. Please check your .env file.")
        return

    runner = InMemoryRunner(
        agent=broken_agent,
        plugins=[LoggingPlugin()] 
    )

    try:
        # This will now run and crash on the LOGIC error (TypeError)
        response = await runner.run_debug(
            "Find papers on 'quantum computing', get a summary, and count the summary."
        )
    except Exception as e:
        print(f"\n✅ Perfect! The agent crashed as expected. Error: {e}")

    print(f"\nTrace saved to '{LOG_FILE_NAME}'. Now run Step 2!")

if __name__ == "__main__":
    asyncio.run(run_broken_agent())