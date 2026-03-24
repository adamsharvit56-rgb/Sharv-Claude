"""Fantasy hockey scoring calculator.

Supports multiple common scoring formats:
- Standard points league
- Category-based (for ranking)
- Custom scoring weights
"""

# Default scoring weights (standard Yahoo/ESPN-style points league)
DEFAULT_SKATER_WEIGHTS = {
    "goals": 3.0,
    "assists": 2.0,
    "points": 0.0,  # Avoid double-counting if goals+assists are scored
    "games_played": 0.0,
}

DEFAULT_GOALIE_WEIGHTS = {
    "wins": 4.0,
    "save_pct": 0.0,  # Handled via bonus thresholds
    "gaa": 0.0,       # Handled via bonus thresholds
    "shutouts": 5.0,
}


def calculate_skater_fantasy_points(player, weights=None):
    """Calculate fantasy points for a projected skater.

    Args:
        player: Dict with projected stats (projected_goals, projected_assists, etc).
        weights: Dict mapping stat name to point value. Uses defaults if None.

    Returns:
        Float total fantasy points.
    """
    w = weights or DEFAULT_SKATER_WEIGHTS
    prefix = "projected_"

    total = 0.0
    for stat, weight in w.items():
        key = f"{prefix}{stat}"
        if key in player:
            total += player[key] * weight
        elif stat in player:
            total += player[stat] * weight
    return round(total, 1)


def calculate_goalie_fantasy_points(goalie, weights=None):
    """Calculate fantasy points for a projected goalie.

    Args:
        goalie: Dict with projected stats.
        weights: Dict mapping stat name to point value. Uses defaults if None.

    Returns:
        Float total fantasy points.
    """
    w = weights or DEFAULT_GOALIE_WEIGHTS
    prefix = "projected_"

    total = 0.0
    for stat, weight in w.items():
        key = f"{prefix}{stat}"
        if key in goalie:
            total += goalie[key] * weight
        elif stat in goalie:
            total += goalie[stat] * weight
    return round(total, 1)


def rank_skaters(projected_skaters, weights=None):
    """Score and rank projected skaters by fantasy points.

    Returns list of (player_dict, fantasy_points) sorted descending.
    """
    scored = []
    for p in projected_skaters:
        fp = calculate_skater_fantasy_points(p, weights)
        scored.append({**p, "fantasy_points": fp})
    scored.sort(key=lambda x: x["fantasy_points"], reverse=True)
    return scored


def rank_goalies(projected_goalies, weights=None):
    """Score and rank projected goalies by fantasy points.

    Returns list of (goalie_dict, fantasy_points) sorted descending.
    """
    scored = []
    for g in projected_goalies:
        fp = calculate_goalie_fantasy_points(g, weights)
        scored.append({**g, "fantasy_points": fp})
    scored.sort(key=lambda x: x["fantasy_points"], reverse=True)
    return scored
