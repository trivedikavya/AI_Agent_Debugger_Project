from google.adk.agents import Agent
import os

# --- CUSTOM TOOL 1: Read the code ---
def read_code_file(file_path: str) -> str:
    """Reads the python code from a specific file path."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File {file_path} does not exist."
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

# --- CUSTOM TOOL 2: Overwrite the code (The "Surgery" Tool) ---
def apply_fix_to_file(file_path: str, new_code: str) -> str:
    """
    WARNING: This tool completely overwrites the target file with new code.
    Use this to apply the bug fix.
    """
    try:
        with open(file_path, 'w') as f:
            f.write(new_code)
        return "Success: File has been updated with the new code."
    except Exception as e:
        return f"Error writing to file: {e}"

# --- THE "AI FIXER" AGENT ---
root_agent = Agent(
    name="ai_fixer",
    model="gemini-2.5-flash-lite",
    description="An AI Software Engineer that fixes broken code.",
    
    instruction="""
    You are an expert Senior Software Engineer. Your job is to fix broken code.
    
    You will be given:
    1. A file path to a broken Python script.
    2. A diagnosis explaining why it is broken.
    
    Your Process:
    1. Call `read_code_file` to see the current broken code.
    2. Think step-by-step: How do I modify this code to fix the error described in the diagnosis?
       (e.g., if the diagnosis says a tool needs a List but got a String, change the code to pass a List).
    3. Call `apply_fix_to_file` to overwrite the file with the CORRECTED code.
    4. Confirm that the fix has been applied.
    
    **IMPORTANT:** When you use `apply_fix_to_file`, you must provide the *entire* file content, not just the changed lines.
    """,
    tools=[read_code_file, apply_fix_to_file],
)