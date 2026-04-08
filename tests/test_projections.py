"""Tests for the projection engine."""

from fantasy_hockey_projections.projections import (
    project_all_skaters,
    project_goalie,
    project_skater,
)


def _sample_skater():
    return {
        "id": 1,
        "name": "Test Player",
        "team": "TST",
        "position": "C",
        "games_played": 41,
        "goals": 20,
        "assists": 30,
        "points": 50,
    }


def _sample_goalie():
    return {
        "id": 2,
        "name": "Test Goalie",
        "team": "TST",
        "games_played": 30,
        "wins": 18,
        "losses": 8,
        "save_pct": 0.920,
        "gaa": 2.50,
        "shutouts": 2,
    }


def test_project_skater_basic():
    player = _sample_skater()
    result = project_skater(player, regression_weight=0.0, target_gp=82)
    assert result["projected_gp"] == 82
    assert result["projected_goals"] == 40
    assert result["projected_assists"] == 60
    assert result["projected_points"] == 100


def test_project_skater_with_regression():
    player = _sample_skater()
    result = project_skater(player, regression_weight=0.15, target_gp=82)
    # With regression, elite player's stats should be pulled slightly down
    assert result["projected_goals"] < 40
    assert result["projected_points"] < 100
    assert result["projected_goals"] > 0


def test_project_skater_zero_games():
    player = _sample_skater()
    player["games_played"] = 0
    result = project_skater(player)
    assert result["projected_goals"] == 0
    assert result["projected_points"] == 0


def test_project_goalie_basic():
    goalie = _sample_goalie()
    result = project_goalie(goalie, regression_weight=0.0, target_gp=55)
    assert result["projected_gp"] == 55
    assert result["projected_wins"] == 33
    assert result["projected_save_pct"] == 0.920
    assert result["projected_gaa"] == 2.50


def test_project_goalie_with_regression():
    goalie = _sample_goalie()
    result = project_goalie(goalie, regression_weight=0.15, target_gp=55)
    # Regression should pull save_pct down and GAA up toward league avg
    assert result["projected_save_pct"] < 0.920
    assert result["projected_gaa"] > 2.50


def test_project_goalie_zero_games():
    goalie = _sample_goalie()
    goalie["games_played"] = 0
    result = project_goalie(goalie)
    assert result["projected_wins"] == 0


def test_project_all_skaters_sorted():
    players = [
        {**_sample_skater(), "name": "Low", "goals": 5, "assists": 5, "points": 10},
        {**_sample_skater(), "name": "High", "goals": 30, "assists": 40, "points": 70},
    ]
    results = project_all_skaters(players, regression_weight=0.0)
    assert results[0]["name"] == "High"
    assert results[1]["name"] == "Low"
