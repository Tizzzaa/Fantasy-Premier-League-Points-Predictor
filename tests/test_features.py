import numpy as np
import pandas as pd
import pytest

from src.features.build_features import rolling_average_calculation


def make_player(element=1, points=(2, 6, 1, 9, 3, 12)):
    """Create one row per gameweek for a synthetic player."""
    n = len(points)
    return pd.DataFrame({
        "element": element,
        "name": f"Player {element}",
        "position": "MID",
        "team": "Test FC",
        "GW": range(1, n + 1),
        "fixture": range(1, n + 1),
        "was_home": [True] * n,
        "total_points": points,
        "minutes": [90] * n,
        "goals_scored": [0] * n,
        "assists": [0] * n,
        "bonus": [0] * n,
        "expected_goals": [0.0] * n,
        "expected_assists": [0.0] * n,
        "clean_sheets": [0] * n,
    })


def make_fixtures(player_df):
    fixture_ids = sorted(player_df["fixture"].unique())
    return pd.DataFrame({
        "id": fixture_ids,
        "team_h_difficulty": [2] * len(fixture_ids),
        "team_a_difficulty": [4] * len(fixture_ids),
    })


def add_features(player_df):
    return rolling_average_calculation(player_df, make_fixtures(player_df))


def test_feature_uses_only_previous_gameweeks():
    """GW4's average is based on GW1-3, not GW4."""
    out = add_features(make_player())

    expected = np.mean([2, 6, 1])
    assert out.loc[3, "total_points_avg_last_5"] == pytest.approx(expected)
    assert out.loc[3, "total_points_avg_last_5"] != pytest.approx(
        np.mean([6, 1, 9])
    )


def test_first_gameweek_has_no_history():
    """The first gameweek has no previous points to average."""
    out = add_features(make_player())

    assert pd.isna(out.loc[0, "total_points_avg_last_5"])


def test_changing_current_week_does_not_change_its_feature():
    """Changing GW5's points affects GW6's feature, but not GW5's."""
    original = add_features(make_player(points=(2, 6, 1, 9, 3, 12)))
    tampered = add_features(make_player(points=(2, 6, 1, 9, 99, 12)))

    assert original.loc[4, "total_points_avg_last_5"] == pytest.approx(
        tampered.loc[4, "total_points_avg_last_5"]
    )
    assert original.loc[5, "total_points_avg_last_5"] != pytest.approx(
        tampered.loc[5, "total_points_avg_last_5"]
    )


def test_history_does_not_leak_between_players():
    """Each player's first gameweek starts without prior history."""
    player_one = make_player(element=1)
    player_two = make_player(element=2, points=(5, 4, 3, 2, 1, 0))
    players = pd.concat([player_one, player_two], ignore_index=True)

    out = add_features(players)

    assert out.loc[[0, 6], "total_points_avg_last_5"].isna().all()
