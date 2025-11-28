from google.adk.agents import Agent
from google.adk.tools import google_search
from typing import List

# --- THE FLAW IS HERE ---
# I added a strict check here. If 'papers' is not a list, it RAISES an error.
# This ensures your log file has a juicy error for the debugger to find.
def count_papers(papers: List[str]) -> str:
    """Counts the number of items in a list of papers."""
    if not isinstance(papers, list):
        # This forces the crash we want!
        raise TypeError(f"Expected a LIST of papers, but got a {type(papers).__name__}.")
        
    count = len(papers)
    return f"Found {count} papers."

# This is the agent that will fail
root_agent = Agent(
    name="broken_researcher",
    model="gemini-2.5-flash-lite",
    description="A researcher that fails at counting.",

    # The instruction remains the same (The Trap)
    instruction="""
    You are a research assistant. You MUST follow these steps:
    1. First, use google_search to find information on a topic.
    2. Second, provide a 50-word summary of the search results.
    3. Third, use the count_papers tool on your 50-word summary to get a count.
    4. Finally, state the summary and the count.
    """,
    tools=[google_search, count_papers],
)