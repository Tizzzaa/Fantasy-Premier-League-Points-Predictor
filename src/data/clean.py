from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw") # Path to the raw data
PROCESSED_DIR = Path("data/processed") # path to the processed data
CLEANED_SSN = ["2024-25","2025-26"]

def clean_merged_gw(season: str):
    """
    Cleans the merged_gw csv including, droping the managers, adding an identifier of the season and dropping the columns realting to the managers
    
    Returns: pd.DataFrame: A dataframe that consists of data for each player in each gameweek
    """
    merged_gw_df = pd.read_csv(RAW_DIR / season / "merged_gw.csv", encoding="latin-1") # Read the csv file in the raw data

    if "position" in merged_gw_df.columns:
        merged_gw_df = merged_gw_df[merged_gw_df["position"] != "MNG"] # Drop all rows where position is MNG
        merged_gw_df = merged_gw_df[merged_gw_df["position"] != "AM"] # Drop all rows where position is AM

    merged_gw_df = merged_gw_df.drop(columns=[c for c in merged_gw_df.columns if c.startswith("mng_")]) # List comprehension that drops all columns that start with "mng_"

    merged_gw_df["season"] = season # creates a new column that tells us what season this is in.
    return merged_gw_df

def clean_fixtures(season: str): 
    """
    Cleans the fixtures csv including, renameing the gw column for consistencey and adding an identifier for the season
        
    Returns: pd.DataFrame: A dataframe that consists of data for each fixture in a season
    """
    fixtures = pd.read_csv(RAW_DIR / season / "fixtures.csv") # Read the csv file in the raw data
    fixtures = fixtures.rename(columns={"event": "GW"}) # Rename the column to GW
    fixtures["season"] = season # add a season column
    return fixtures

def clean_teams(season: str): 
    """
    Cleans the teams csv by adding an identifier for the season            

    Returns: pd.DataFrame: A dataframe that consists of data for each teamn
    """
    teams = pd.read_csv(RAW_DIR / season / "teams.csv") # Read the csv file in the raw data
    teams["season"] = season # add a season column
    return teams


def clean_current_ssn():
    """
    Cleans the csv for the current season by merging the csvs (history, teams, players) and making the csv consistent with previous seasons.            

    Returns: pd.DataFrame: A dataframe that consists of data for each team
    """
    
    history = pd.read_csv(RAW_DIR / "2026-27" / "history.csv") # Read the csv for history
    teams = pd.read_csv(RAW_DIR / "2026-27" / "teams.csv") # Read the csv for teams
    players = pd.read_csv(RAW_DIR / "2026-27" / "players.csv") # Read the csv for players

    players = players[["id", "web_name", "element_type", "team"]].rename(columns={"id": "element", "web_name": "name", "team": "team_id"}) # Slecting the needed columns and renaming them for consistencey
    players["position"] = players["element_type"].map({1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}) # Assigning names to the player positions for consistencey
    players = players.drop(columns="element_type") # deleting redundent position identifier

    team_names = teams.set_index("id")["name"] # create a lookup table for teamID to team names
    players["team"] = players["team_id"].map(team_names) # map the team id to the team name and add that column to players

    prior_length = len(history) # Store the prior length of history
    merged = history.merge(players, on="element", how="left", validate="many_to_one") # Merge history data frame and players dataframe into merged dataframe
    assert len(merged) == prior_length, "Merge changed the row count" # If the row count of the dataframe has changed (it shouldnt) throw an error

    merged["opponent"] = merged["opponent_team"].map(team_names) # Adding string opponent column for readibilty later

    merged.rename(columns={"round": "GW"}) # Rename round to gw for consistencey
    merged["season"] = "2026-27" # Adding season to identify between other seasons data.

    return merged

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True) # creating a new processed directory if it does not already exist

    for season_dir in CLEANED_SSN: #loops through each season in the raw data folder
        if not (RAW_DIR / season_dir).is_dir(): # If something is not a folder it is skipped
            continue
        season_data = clean_merged_gw(season_dir) # Create a dataframe with the clean merged data
        fixtures = clean_fixtures(season_dir)
        teams = clean_teams(season_dir)
        out_path_season_data = PROCESSED_DIR / f"{season_dir}_gw.csv" # The path where the gw data is sent
        out_path_fixtures = PROCESSED_DIR / f"{season_dir}_fixtures.csv" # The path where the fixture data is sent
        out_path_teams = PROCESSED_DIR / f"{season_dir}_teams.csv" # # The path where the team data is sent
        season_data.to_csv(out_path_season_data, index=False) # Send the gws df to the path given as a csv
        fixtures.to_csv(out_path_fixtures, index=False) # Send the fixtures df to the path given as a csv
        teams.to_csv(out_path_teams, index=False) # Send the teams df to the path given as a csv
        print(f"Saved {out_path_season_data} ({len(season_data)} rows)") 
    
    current_season_data = clean_current_ssn() # Create a dataframe with the clean merged data
    out_path_current_season_data = PROCESSED_DIR / f"2026-27_gw.csv" # The path where the current season data is sent
    current_season_data.to_csv(out_path_current_season_data, index=False) # Send the current season df to the path given as a csv
    print(f"Saved {out_path_current_season_data} ({len(current_season_data)} rows)") 


if __name__ == "__main__":
    main()