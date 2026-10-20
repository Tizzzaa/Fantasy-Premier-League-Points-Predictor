from pathlib import Path
import requests
import urllib.request
print(urllib.request.urlopen("https://raw.githubusercontent.com").status)

BASE_URL = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data" #URL for the fpl data

SEASONS = ["2024-25", "2025-26"] # Enter the seasons you want the data for in this array
FILES = ["gws/merged_gw.csv", "fixtures.csv", "teams.csv"] # Entehr the data you want from this season

RAW_DIR = Path("data/raw") # the directory containing the raw data


def download_file(season: str, file_path: str) -> None:
    url = f"{BASE_URL}/{season}/{file_path}" # The url that the code is going to scrape
    dest = RAW_DIR / season / Path(file_path).name # The destination of where the data will be stored

    if dest.exists(): # If there is already this file at this location
        print(f"Skipping {dest} (already downloaded)")
        return

    dest.parent.mkdir(parents=True, exist_ok=True) # If it does not already exist, create a parent folder for this file

    response = requests.get(url, timeout=30) # Scrape the data from the github repo
    response.raise_for_status() # Fail loudly

    dest.write_bytes(response.content) # Write the content of the data into the file
    print(f"Saved {dest}")


def main() -> None:
    for season in SEASONS:
        for file_path in FILES: # Repeat the process for each file and each season
            download_file(season, file_path)


if __name__ == "__main__":
    main()