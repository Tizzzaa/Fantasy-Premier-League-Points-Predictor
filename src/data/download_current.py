import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

BASE = "https://fantasy.premierleague.com/api" # Base URL of the FPL API where we get our data from
OUT_DIR = Path("data/raw/2026-27")


def get_fpl_json(path: str) -> dict | list: # Function to fetch the data from fpl
    req = urllib.request.Request(f"{BASE}/{path}", headers={"User-Agent": "Mozilla/5.0"}) # Building the request which will be sent to the API
    try: # Checking if the data is recieved correctly
        with urllib.request.urlopen(req, timeout=30) as r: # Sending the request to the api and storing the returned data in r
            return json.load(r) # Return the recieved data as a python data

    except urllib.error.HTTPError as error: # Catches Http return error
        raise RuntimeError(f"Http Error {error.code} while reuesting API data") from error


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True) # Creating the output directory if it does not already exist

    boot = get_fpl_json("bootstrap-static/") # Collect the data from the correct api
    players = pd.DataFrame(boot["elements"]) # Create a data frame for the players
    teams = pd.DataFrame(boot["teams"]) # Create a dataframe for the teams
    fixtures = pd.DataFrame(get_fpl_json("fixtures/")) # Create a dataframe for the fixtures
    players.to_csv(OUT_DIR / "players.csv", index=False) # Convert the players dataframe to a csv and send it to out directory
    teams.to_csv(OUT_DIR / "teams.csv", index=False) # Convert the teams dataframe to a csv and send it to out directory
    fixtures.to_csv(OUT_DIR / "fixtures.csv", index=False)# Convert the fixtures dataframe to a csv and send it to out directory

    rows = []
    for pid in players["id"]: # For each player that has an id
        history = get_fpl_json(f"element-summary/{pid}/")["history"] # Get the JSON for that individual player
        rows.extend(history) # Add that row the the history tables
        time.sleep(0.2)            # Do not overload the api

    historydf = pd.DataFrame(rows)# Create a data frame for the history
    historydf.to_csv(OUT_DIR / "history.csv", index=False) # Convert the history dataframe to a csv and send it to out directory
    print(f"Saved {len(rows)} player-gameweek rows")


if __name__ == "__main__":
    main()