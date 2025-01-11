import requests

# Tool: Fetch Meeting Notes
def fetch_meeting_notes(meeting_id):
    # Mock API call for meeting notes
    return f"Meeting {meeting_id}: Discussed Q4 strategies and portfolio adjustments."

# Tool: Create Trello Task
def create_trello_task(task_name, description):
    trello_api_key = "your_trello_api_key"
    trello_token = "your_trello_token"
    list_id = "your_trello_list_id"

    url = f"https://api.trello.com/1/cards"
    payload = {
        "key": trello_api_key,
        "token": trello_token,
        "idList": list_id,
        "name": task_name,
        "desc": description
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return f"Trello Task Created: {response.json().get('name')}"
    else:
        return f"Failed to create Trello task: {response.text}"

# Tool: Fetch Market Data
def fetch_market_data(ticker):
    # Mock API call for market data
    return f"Market Data for {ticker}: Price = $150.23, Change = +1.5%."
