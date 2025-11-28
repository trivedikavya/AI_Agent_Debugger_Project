from google.adk.agents import Agent
from google.adk.tools import google_search
from typing import List

# --- THE FLAW IS HERE ---
def count_papers(papers: List[str]) -> str:
    """Counts the number of items in a list of papers."""
    
    # 1. We strictly check if it is a list.
    if not isinstance(papers, list):
        # 2. FORCE THE CRASH: If it's a string, we RAISE an error.
        # This ensures your log file captures a "TypeError" for the debugger to find.
        raise TypeError(f"Expected a LIST of papers, but got a {type(papers).__name__}: '{papers}'")
        
    count = len(papers)
    return f"Found {count} papers."

# This is the agent that will fail
root_agent = Agent(
    name="broken_researcher",
    model="gemini-2.5-flash-lite",
    description="A researcher that fails at counting.",

    # THE TRAP: This instruction tricks the agent into passing a string summary
    # to the count_papers tool, which now STRICTLY requires a list.
    instruction="""
    You are a research assistant. You MUST follow these steps:
    1. First, use google_search to find information on a topic.
    2. Second, provide a 50-word summary of the search results.
    3. Third, use the count_papers tool on your 50-word summary to get a count.
    4. Finally, state the summary and the count.
    """,
    tools=[google_search, count_papers],
)