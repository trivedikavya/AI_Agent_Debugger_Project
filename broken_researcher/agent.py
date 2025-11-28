from google.adk.agents import Agent
from google.adk.tools import google_search
from typing import List

# --- THE FLAW IS HERE ---
# This tool is built correctly. It requires a LIST of strings.
def count_papers(papers: List[str]) -> str:
    """Counts the number of items in a list of papers."""
    try:
        count = len(papers)
        return f"Found {count} papers."
    except TypeError:
        return "Error: I was given something that wasn't a list."

# This is the agent that will fail
root_agent = Agent(
    name="broken_researcher",
    model="gemini-2.5-flash-lite",
    description="A researcher that fails at counting.",

    # THE FLAW IS ALSO HERE
    # This instruction *tricks* the agent.
    # It tells it to get a "summary" (a string) and then
    # use `count_papers` (which needs a list) on that summary.
    # This will cause a 'TypeError' because you can't get the 'len()' of a string
    # in the way the tool expects.
    instruction="""
    You are a research assistant. You MUST follow these steps:
    1. First, use google_search to find information on a topic.
    2. Second, provide a 50-word summary of the search results.
    3. Third, use the count_papers tool on your 50-word summary to get a count.
    4. Finally, state the summary and the count.
    """,
    tools=[google_search, count_papers],
)