from google.adk.agents import Agent
import re  # We will use this to find errors in the log

# --- CUSTOM TOOL 1: Read the log file ---
def read_log_file(file_path: str) -> str:
    """
    Reads the content of a specified log file and returns the last 4000
    characters as a string.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if len(content) > 4000:
            return content[-4000:]
        else:
            return content
            
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"Error reading file: {e}"

# --- CUSTOM TOOL 2: Find the error in the log ---
def find_last_error_in_trace(log_content: str) -> str:
    """
    Analyzes a log trace to find the last tool call and any
    Traceback or ERROR messages. Returns the relevant snippets.
    """
    # Try to find a full Python crash log (Traceback)
    # re.DOTALL makes '.' match newlines
    error_trace = re.findall(r"Traceback \(most recent call last\):(.+)", log_content, re.DOTALL)
    
    if error_trace:
        # Get the last traceback and return the last 1000 chars of it
        return f"Found a hard crash (Traceback): \n...{error_trace[-1][-1000:]}"
    
    # If no crash, find the last tool call and its result
    # This looks for the text between "TOOL STARTING" and the next "[logging_plugin]"
    tool_calls = re.findall(r"\[logging_plugin\] 🔧 TOOL STARTING(.*?)\[logging_plugin\]", log_content, re.DOTALL)
    tool_results = re.findall(r"\[logging_plugin\] 🔧 TOOL COMPLETED(.*?)\[logging_plugin\]", log_content, re.DOTALL)
    
    if not tool_calls:
        return "No tool calls found in the log."
    
    # Get the last tool call
    last_call_snippet = tool_calls[-1]
    
    # Get the last tool result (if one exists)
    last_result_snippet = "No 'TOOL COMPLETED' log found. The agent probably crashed."
    if tool_results:
        last_result_snippet = tool_results[-1]
    
    return f"""
    Here is the snippet for the last tool call:
    {last_call_snippet}
    
    Here is the snippet for that tool's result:
    {last_result_snippet}
    """

# --- THE "AI MECHANIC" AGENT ---
root_agent = Agent(
    name="ai_debugger",
    model="gemini-2.5-flash-lite",
    description="An AI assistant that debugs agent trace logs.",
    
    # This instruction is the "brain" of your agent.
    # It tells the agent HOW to think.
    instruction="""
    You are an expert AI Agent Debugger. Your job is to help a developer
    understand why their agent failed. The user will give you a file path.

    You MUST follow these steps:
    1.  Use the `read_log_file` tool to get the log's content.
    2.  Use the `find_last_error_in_trace` tool on the log content to
        pinpoint the exact tool call that failed.
    3.  Carefully analyze the "Last Tool Call" and "Last Tool Result" snippets.
    4.  Based on your analysis, provide a simple, plain-English
        diagnosis of the *root cause* of the problem.
    
    **DO NOT just repeat the log.** Explain the *reason* for the error.

    **Example Diagnosis (for a type mismatch):**
    "DIAGNOSIS: The agent failed because it tried to call the `count_papers` tool
    with a single `string` of text. However, the `count_papers` tool is
    built to expect a `list` of items. This mismatch caused a TypeError."
    
    **Example Diagnosis (for a missing tool):**
    "DIAGNOSIS: The agent failed because it tried to call a tool named
    `find_hotels`, but this tool was not provided to the agent."
    """,
    tools=[read_log_file, find_last_error_in_trace],
)