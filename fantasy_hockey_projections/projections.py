"""Projection engine for fantasy hockey stats.

Uses pace-based projection: extrapolates current per-game rates to a full
82-game season, with optional regression toward league-average rates.
"""

FULL_SEASON_GP = 82

# League-average per-game rates (approximate) for regression
LEAGUE_AVG_GOALS_PER_GAME = 0.30
LEAGUE_AVG_ASSISTS_PER_GAME = 0.48
LEAGUE_AVG_POINTS_PER_GAME = 0.78

LEAGUE_AVG_GOALIE_WINS_PER_GAME = 0.50
LEAGUE_AVG_SAVE_PCT = 0.905
LEAGUE_AVG_GAA = 2.95
LEAGUE_AVG_SHUTOUTS_PER_GAME = 0.05


def project_skater(player, regression_weight=0.15, target_gp=FULL_SEASON_GP):
    """Project a skater's stats to a full season.

    Args:
        player: Dict with keys: name, team, position, games_played, goals,
                assists, points.
        regression_weight: How much to regress toward league average (0-1).
            0 = pure pace projection, 1 = fully regressed to league avg.
        target_gp: Number of games to project to.

    Returns:
        Dict with projected stats.
    """
    gp = player["games_played"]
    if gp == 0:
        return {**player, "projected_goals": 0, "projected_assists": 0,
                "projected_points": 0, "projected_gp": 0}

    goals_pg = player["goals"] / gp
    assists_pg = player["assists"] / gp
    points_pg = player["points"] / gp

    # Regress toward league average
    adj_goals_pg = (1 - regression_weight) * goals_pg + regression_weight * LEAGUE_AVG_GOALS_PER_GAME
    adj_assists_pg = (1 - regression_weight) * assists_pg + regression_weight * LEAGUE_AVG_ASSISTS_PER_GAME
    adj_points_pg = (1 - regression_weight) * points_pg + regression_weight * LEAGUE_AVG_POINTS_PER_GAME

    return {
        **player,
        "projected_gp": target_gp,
        "projected_goals": round(adj_goals_pg * target_gp),
        "projected_assists": round(adj_assists_pg * target_gp),
        "projected_points": round(adj_points_pg * target_gp),
    }


def project_goalie(goalie, regression_weight=0.15, target_gp=None):
    """Project a goalie's stats to a full season.

    Args:
        goalie: Dict with keys: name, team, games_played, wins, losses,
                save_pct, gaa, shutouts.
        regression_weight: How much to regress toward league average (0-1).
        target_gp: Target games played (defaults to pace-based estimate).

    Returns:
        Dict with projected stats.
    """
    gp = goalie["games_played"]
    if gp == 0:
        return {**goalie, "projected_wins": 0, "projected_save_pct": 0.0,
                "projected_gaa": 0.0, "projected_shutouts": 0, "projected_gp": 0}

    if target_gp is None:
        # Estimate starter vs backup: project based on pace
        target_gp = round(gp * (FULL_SEASON_GP / max(gp, 1)))
        target_gp = min(target_gp, 65)  # Cap at realistic max

    wins_pg = goalie["wins"] / gp
    shutouts_pg = goalie["shutouts"] / gp

    adj_wins_pg = (1 - regression_weight) * wins_pg + regression_weight * LEAGUE_AVG_GOALIE_WINS_PER_GAME
    adj_save_pct = (1 - regression_weight) * goalie["save_pct"] + regression_weight * LEAGUE_AVG_SAVE_PCT
    adj_gaa = (1 - regression_weight) * goalie["gaa"] + regression_weight * LEAGUE_AVG_GAA
    adj_shutouts_pg = (1 - regression_weight) * shutouts_pg + regression_weight * LEAGUE_AVG_SHUTOUTS_PER_GAME

    return {
        **goalie,
        "projected_gp": target_gp,
        "projected_wins": round(adj_wins_pg * target_gp),
        "projected_save_pct": round(adj_save_pct, 3),
        "projected_gaa": round(adj_gaa, 2),
        "projected_shutouts": round(adj_shutouts_pg * target_gp),
    }


def project_all_skaters(players, regression_weight=0.15, target_gp=FULL_SEASON_GP):
    """Project a list of skaters and sort by projected points descending."""
    projected = [project_skater(p, regression_weight, target_gp) for p in players]
    projected.sort(key=lambda p: p["projected_points"], reverse=True)
    return projected


def project_all_goalies(goalies, regression_weight=0.15):
    """Project a list of goalies and sort by projected wins descending."""
    projected = [project_goalie(g, regression_weight) for g in goalies]
    projected.sort(key=lambda g: g["projected_wins"], reverse=True)
    return projected
