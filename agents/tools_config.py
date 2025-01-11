from langchain.tools import tool
from tools import fetch_meeting_notes, create_trello_task, fetch_market_data

# Define tools
@tool
def meeting_notes_tool(meeting_id: str) -> str:
    """Fetch meeting notes for a given meeting ID."""
    return fetch_meeting_notes(meeting_id)

@tool
def trello_task_tool(task_name: str, description: str) -> str:
    """Create a Trello task with the given name and description."""
    return create_trello_task(task_name, description)

@tool
def market_data_tool(ticker: str) -> str:
    """Fetch market data for a given stock ticker."""
    return fetch_market_data(ticker)

# Register tools
TOOLS = [meeting_notes_tool, trello_task_tool, market_data_tool]
