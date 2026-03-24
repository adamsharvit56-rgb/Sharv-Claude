"""Fetch NHL player statistics from the NHL API."""

import requests

NHL_API_BASE = "https://api-web.nhle.com"


def get_skater_stats(season="20242025", game_type=2, limit=100):
    """Fetch skater stats for a given season.

    Args:
        season: NHL season identifier (e.g. "20242025" for 2024-25).
        game_type: 2 for regular season, 3 for playoffs.
        limit: Maximum number of players to return.

    Returns:
        List of player stat dicts.
    """
    url = (
        f"{NHL_API_BASE}/v1/skater-stats-leaders/current"
        f"?categories=points&limit={limit}"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    leaders = data.get("points", [])

    players = []
    for entry in leaders:
        players.append({
            "id": entry.get("id"),
            "name": f"{entry.get('firstName', {}).get('default', '')} {entry.get('lastName', {}).get('default', '')}",
            "team": entry.get("teamAbbrev", {}).get("default", ""),
            "position": entry.get("positionCode", ""),
            "games_played": entry.get("gamesPlayed", 0),
            "goals": entry.get("goals", 0),
            "assists": entry.get("assists", 0),
            "points": entry.get("points", 0),
        })
    return players


def get_goalie_stats(limit=30):
    """Fetch goalie stats leaders.

    Args:
        limit: Maximum number of goalies to return.

    Returns:
        List of goalie stat dicts.
    """
    url = (
        f"{NHL_API_BASE}/v1/goalie-stats-leaders/current"
        f"?categories=wins&limit={limit}"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    leaders = data.get("wins", [])

    goalies = []
    for entry in leaders:
        goalies.append({
            "id": entry.get("id"),
            "name": f"{entry.get('firstName', {}).get('default', '')} {entry.get('lastName', {}).get('default', '')}",
            "team": entry.get("teamAbbrev", {}).get("default", ""),
            "games_played": entry.get("gamesPlayed", 0),
            "wins": entry.get("wins", 0),
            "losses": entry.get("losses", 0),
            "save_pct": entry.get("savePctg", 0.0),
            "gaa": entry.get("goalsAgainstAverage", 0.0),
            "shutouts": entry.get("shutouts", 0),
        })
    return goalies


def build_sample_skaters():
    """Return sample skater data for offline/testing use."""
    return [
        {"id": 8478402, "name": "Connor McDavid", "team": "EDM", "position": "C",
         "games_played": 78, "goals": 44, "assists": 76, "points": 120},
        {"id": 8479318, "name": "Auston Matthews", "team": "TOR", "position": "C",
         "games_played": 74, "goals": 51, "assists": 38, "points": 89},
        {"id": 8477934, "name": "Leon Draisaitl", "team": "EDM", "position": "C",
         "games_played": 81, "goals": 41, "assists": 65, "points": 106},
        {"id": 8480069, "name": "Cale Makar", "team": "COL", "position": "D",
         "games_played": 77, "goals": 21, "assists": 69, "points": 90},
        {"id": 8478550, "name": "Mikko Rantanen", "team": "COL", "position": "RW",
         "games_played": 80, "goals": 42, "assists": 63, "points": 105},
        {"id": 8479323, "name": "David Pastrnak", "team": "BOS", "position": "RW",
         "games_played": 82, "goals": 47, "assists": 50, "points": 97},
        {"id": 8476453, "name": "Nikita Kucherov", "team": "TBL", "position": "RW",
         "games_played": 81, "goals": 44, "assists": 56, "points": 100},
        {"id": 8477492, "name": "Nathan MacKinnon", "team": "COL", "position": "C",
         "games_played": 82, "goals": 39, "assists": 61, "points": 100},
        {"id": 8480010, "name": "Quinn Hughes", "team": "VAN", "position": "D",
         "games_played": 82, "goals": 17, "assists": 75, "points": 92},
        {"id": 8478483, "name": "Mitch Marner", "team": "TOR", "position": "RW",
         "games_played": 82, "goals": 26, "assists": 59, "points": 85},
    ]


def build_sample_goalies():
    """Return sample goalie data for offline/testing use."""
    return [
        {"id": 8479406, "name": "Connor Hellebuyck", "team": "WPG",
         "games_played": 60, "wins": 37, "losses": 16, "save_pct": 0.921, "gaa": 2.39, "shutouts": 4},
        {"id": 8478048, "name": "Ilya Sorokin", "team": "NYI",
         "games_played": 55, "wins": 30, "losses": 18, "save_pct": 0.915, "gaa": 2.65, "shutouts": 3},
        {"id": 8477424, "name": "Igor Shesterkin", "team": "NYR",
         "games_played": 58, "wins": 33, "losses": 17, "save_pct": 0.918, "gaa": 2.52, "shutouts": 5},
    ]
