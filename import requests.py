import requests
import json

# Endpoint for NFL ADP data on Sleeper
url = "https://api.sleeper.app/v1/players/nfl/adp"

# Optional: Add query parameters for format or season
params = {
    "season": 2025,     # Replace with current or desired season
    "position": "ALL",  # You can filter by QB, RB, WR, etc.
    "ppr": "half"       # ADP varies by scoring format (true for PPR leagues)
}

# Make the request
response = requests.get(url, params=params)

# Parse the response
if response.status_code == 200:
    data = response.json()
    # Example: print first 10 players with ADP
    for player in data[:10]:
        name = player.get("full_name", "N/A")
        adp = player.get("adp", "N/A")
        team = player.get("team", "N/A")
        print(f"{name} ({team}) - ADP: {adp}")
else:
    print("Error fetching data:", response.status_code)