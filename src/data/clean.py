from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw") # Path to the raw data
PROCESSED_DIR = Path("data/processed") # path to the processed data


def clean_merged_gw(season: str) -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / season / "merged_gw.csv", encoding="latin-1") # Read the csv file in the raw data

    if "position" in df.columns:
        df = df[df["position"] != "MNG"] # Drop all rows where position is MNG
        df = df[df["position"] != "AM"] # Drop all rows where position is AM

    df = df.drop(columns=[c for c in df.columns if c.startswith("mng_")]) # List comprehension that drops all columns that start with "mng_"

    df["season"] = season # creates a new column that tells us what season this is in.
    return df

def clean_fixtures(season: str) -> pd.DataFrame: 
    df = pd.read_csv(RAW_DIR / season / "fixtures.csv") # Read the csv file in the raw data
    df = df.rename(columns={"event": "GW"}) # Rename the column to GW
    df["season"] = season # add a season column
    return df

def clean_teams(season: str) -> pd.DataFrame: 
    df = pd.read_csv(RAW_DIR / season / "teams.csv") # Read the csv file in the raw data
    df["season"] = season # add a season column
    return df

def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True) # creating a new processed directory if it does not already exist

    for season_dir in sorted(RAW_DIR.iterdir()): #loops through each season in the raw data folder
        if not season_dir.is_dir(): # If something is not a folder it is skipped
            continue
        df = clean_merged_gw(season_dir.name) # Create a dataframe with the clean merged data
        dff = clean_fixtures(season_dir.name)
        dft = clean_teams(season_dir.name)
        out_path = PROCESSED_DIR / f"{season_dir.name}_gw.csv" # The path where the gw data is sent
        out_pathf = PROCESSED_DIR / f"{season_dir.name}_fixtures.csv" # The path where the fixture data is sent
        out_patht = PROCESSED_DIR / f"{season_dir.name}_teams.csv" # # The path where the team data is sent
        df.to_csv(out_path, index=False) # Send the gws df to the path given as a csv
        dff.to_csv(out_pathf, index=False) # Send the fixtures df to the path given as a csv
        dft.to_csv(out_patht, index=False) # Send the teams df to the path given as a csv
        print(f"Saved {out_path} ({len(df)} rows)") 


if __name__ == "__main__":
    main()