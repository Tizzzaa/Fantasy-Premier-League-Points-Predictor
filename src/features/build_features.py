import pandas as pd
import os
from pathlib import Path
from sklearn.metrics import mean_absolute_error, root_mean_squared_error


def rolling_average_calculation(player_df, fixture_df,windows=[5]):
    """
    This is a function that takes in a data frame as an input, and returns the average stats for every play for the last n matches for every gameweek
    
    Returns: pd.DataFrame: containing the calculated average stats for the player.
    """

    player_df = player_df.sort_values(["element","GW"]).copy()
    player_df = player_df[["element","name","position","team","minutes","goals_scored","assists", "was_home","bonus", "expected_goals", "expected_assists", "clean_sheets", "total_points","fixture"]]
    stats_players = ["minutes","difficulty","goals_scored","assists", "bonus", "expected_goals", "expected_assists", "clean_sheets", "difficulty","total_points"]
    fixture_lookup = fixture_df.set_index("id")

    player_df["difficulty"] = player_df["fixture"].map(fixture_lookup["team_h_difficulty"]).where(player_df["was_home"],player_df["fixture"].map(fixture_lookup["team_a_difficulty"]),)
    player_groups = player_df.groupby("element")
    for w in windows:
        for stat in stats_players:
            player_df[f"{stat}_avg_last_{w}"] = player_groups[stat].transform(lambda s: s.shift(1).rolling(w, min_periods=1).mean())

    return player_df


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    BASE_DIR = os.path.sep.join(current_dir.split(os.path.sep)[:-2])
    player_df = pd.read_csv(Path(BASE_DIR) / "data" / "processed" / "2025-26_gw.csv")
    fixture_df = pd.read_csv(Path(BASE_DIR) / "data" / "processed" / "2025-26_fixtures.csv")
    average_stats = rolling_average_calculation(player_df,fixture_df)

    average_stats = average_stats.dropna(subset=["total_points_avg_last_5"])

    mean_abs_error = mean_absolute_error(average_stats["total_points"],average_stats["total_points_avg_last_5"])
    root_mean_squ_error = root_mean_squared_error(average_stats["total_points"],average_stats["total_points_avg_last_5"])

    print(mean_abs_error)
    print(root_mean_squ_error)