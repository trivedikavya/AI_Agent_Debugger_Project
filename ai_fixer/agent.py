from google.adk.agents import Agent
import os

# --- TOOLS REMAIN THE SAME ---
def read_code_file(file_path: str) -> str:
    """Reads the python code from a specific file path."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File {file_path} does not exist."
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def apply_fix_to_file(file_path: str, new_code: str) -> str:
    """
    WARNING: This tool completely overwrites the target file with new code.
    """
    try:
        with open(file_path, 'w') as f:
            f.write(new_code)
        return "Success: File has been updated with the new code."
    except Exception as e:
        return f"Error writing to file: {e}"

# --- UPDATED AGENT ---
root_agent = Agent(
    name="ai_fixer",
    model="gemini-2.5-flash-lite",
    description="An AI Software Engineer that fixes broken code.",
    
    # --- STRONGER INSTRUCTIONS ---
    instruction="""
    You are an autonomous AI Software Engineer. Your goal is to FIX a broken file.
    
    You will receive:
    1. A target file path.
    2. A diagnosis of the error.

    **YOUR MANDATORY CHECKLIST:**
    1. Call `read_code_file` to get the current content.
    2. Analyze the code and the diagnosis. Find the specific line causing the error.
    3. Rewrite the code to fix the logic error.
    4. **CRITICAL:** You MUST call the `apply_fix_to_file` tool to save your changes.
       - Do NOT just print the code.
       - Do NOT ask for permission.
       - Call the tool immediately with the COMPLETE fixed code.
    
    If the diagnosis mentions a "TypeError" about a list vs string, modify the code 
    to ensure a list is passed (e.g., wrap the string in brackets `[summary]`).
    """,
    tools=[read_code_file, apply_fix_to_file],
)