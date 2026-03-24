"""Tests for the fantasy scoring calculator."""

from fantasy_hockey_projections.scoring import (
    calculate_goalie_fantasy_points,
    calculate_skater_fantasy_points,
    rank_skaters,
)


def _projected_skater(goals=30, assists=40):
    return {
        "name": "Test",
        "team": "TST",
        "position": "C",
        "games_played": 82,
        "goals": goals,
        "assists": assists,
        "points": goals + assists,
        "projected_gp": 82,
        "projected_goals": goals,
        "projected_assists": assists,
        "projected_points": goals + assists,
    }


def _projected_goalie(wins=35, shutouts=4):
    return {
        "name": "Test G",
        "team": "TST",
        "games_played": 55,
        "wins": wins,
        "losses": 15,
        "save_pct": 0.918,
        "gaa": 2.50,
        "shutouts": shutouts,
        "projected_gp": 55,
        "projected_wins": wins,
        "projected_save_pct": 0.918,
        "projected_gaa": 2.50,
        "projected_shutouts": shutouts,
    }


def test_skater_fantasy_points_default():
    p = _projected_skater(goals=30, assists=40)
    # Default: goals=3, assists=2 => 30*3 + 40*2 = 170
    fp = calculate_skater_fantasy_points(p)
    assert fp == 170.0


def test_skater_fantasy_points_custom_weights():
    p = _projected_skater(goals=30, assists=40)
    weights = {"goals": 5.0, "assists": 3.0, "points": 0.0, "games_played": 0.0}
    fp = calculate_skater_fantasy_points(p, weights)
    assert fp == 270.0  # 30*5 + 40*3


def test_goalie_fantasy_points_default():
    g = _projected_goalie(wins=35, shutouts=4)
    # Default: wins=4, shutouts=5 => 35*4 + 4*5 = 160
    fp = calculate_goalie_fantasy_points(g)
    assert fp == 160.0


def test_rank_skaters_ordering():
    players = [
        _projected_skater(goals=10, assists=15),
        _projected_skater(goals=40, assists=50),
    ]
    ranked = rank_skaters(players)
    assert ranked[0]["projected_goals"] == 40
    assert ranked[1]["projected_goals"] == 10
    assert ranked[0]["fantasy_points"] > ranked[1]["fantasy_points"]
