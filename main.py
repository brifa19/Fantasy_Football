import subprocess
import pandas as pd
from io import StringIO
import json

rscript_path = "C:\\Program Files\\R-aarch64\\R-4.5.1\\bin\\Rscript.exe"
r_script = "scrape_fantasypros.r"

try:
    result = subprocess.run(
        [rscript_path, r_script],
        capture_output=True,
        text=True,
        encoding='utf-8',
        check=True
    )

    raw_output = result.stdout.strip()

    # Save to file for inspection
    with open("debug_r_output.json", "w", encoding="utf-8") as f:
        f.write(raw_output)

    print("Raw R output saved to debug_r_output.json")
    print("First 500 chars:\n", raw_output[:500])

    # Validate JSON first
    try:
        json.loads(raw_output)  # Check for validity
    except json.JSONDecodeError as e:
        print("❌ JSON is invalid or truncated!")
        raise e

    # Proper way to read JSON into DataFrame
    rankings_df = pd.read_json(StringIO(raw_output))
    rankings_df.drop(columns=["fantasypros_id", "rank", "player_eligibility", "player_page_url", "player_filename", "player_owned_avg", "player_ecr_delta"], inplace=True)

except subprocess.CalledProcessError as e:
    print("❌ R script execution failed.")
    print("STDERR:\n", e.stderr)
except Exception as ex:
    print("❌ Unexpected Python error:", ex)

import requests
import pandas as pd

# API URL
url = "https://www.beatadp.com/api/base-rankings"
params = {
    "draftType": "REDRAFT",
    "scoringFormat": "HALF_PPR",
    "platform": "SLEEPER",
    "qbType": "1QB"
}

# Fetch the data
response = requests.get(url, params=params)
data = response.json()

# Flatten everything in one go, including fantasyPlayer.*
df = pd.json_normalize(
    data,
    record_path="playerRankings",
    meta=[["id"]],
    meta_prefix="root_",
    sep=".",
    record_prefix="",  # Avoid extra prefixes for playerRankings
    max_level=2        # Ensures nested fantasyPlayer.* is expanded
)

# Clean up column names (optional)
df.rename(columns={
    "fantasyPlayer.name": "player_name",
    "fantasyPlayer.position": "position",
    "fantasyPlayer.team": "team",
    "fantasyPlayer.fullName": "full_name"
}, inplace=True)

df.drop(columns=["id", 
                 "platformRankingsId",
                   "fantasyPlayerId",
                     "attribute",
                       "auctionValue",
                       "createdAt",
                       "fantasyPlayer.id",
                       "fantasyPlayer.sleeperId",
          S             "fantasyPlayer.yahooId",
                       "fantasyPlayer.espnId",
                       "fantasyPlayer.lastUpdated",
                       "root_id",
                       "tier"], inplace=True)  # Drop the root ID column if not needed

# Save
df.to_csv("beatadp_rankings_clean.csv", index=False)

combined_df = rankings_df.merge(
    df, on="player_name", how="left")

combined_df["ecr_vs_adp"] = (combined_df["overallRank"] - combined_df["ecr"]).round(0)