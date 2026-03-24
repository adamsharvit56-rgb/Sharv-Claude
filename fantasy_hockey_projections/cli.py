"""Command-line interface for fantasy hockey projections."""

import argparse
import sys

from fantasy_hockey_projections.fetcher import (
    build_sample_goalies,
    build_sample_skaters,
    get_goalie_stats,
    get_skater_stats,
)
from fantasy_hockey_projections.projections import (
    project_all_goalies,
    project_all_skaters,
)
from fantasy_hockey_projections.scoring import rank_goalies, rank_skaters


def format_skater_table(ranked_skaters, top_n=25):
    """Format ranked skaters as a text table."""
    header = (
        f"{'Rank':<5} {'Player':<25} {'Pos':<4} {'Team':<5} "
        f"{'pGP':<5} {'pG':<5} {'pA':<5} {'pPTS':<6} {'FPts':<7}"
    )
    lines = [header, "-" * len(header)]

    for i, p in enumerate(ranked_skaters[:top_n], start=1):
        lines.append(
            f"{i:<5} {p['name']:<25} {p.get('position', ''):<4} {p['team']:<5} "
            f"{p['projected_gp']:<5} {p['projected_goals']:<5} "
            f"{p['projected_assists']:<5} {p['projected_points']:<6} "
            f"{p['fantasy_points']:<7}"
        )
    return "\n".join(lines)


def format_goalie_table(ranked_goalies, top_n=15):
    """Format ranked goalies as a text table."""
    header = (
        f"{'Rank':<5} {'Player':<25} {'Team':<5} "
        f"{'pGP':<5} {'pW':<5} {'pSV%':<7} {'pGAA':<6} {'pSO':<5} {'FPts':<7}"
    )
    lines = [header, "-" * len(header)]

    for i, g in enumerate(ranked_goalies[:top_n], start=1):
        lines.append(
            f"{i:<5} {g['name']:<25} {g['team']:<5} "
            f"{g['projected_gp']:<5} {g['projected_wins']:<5} "
            f"{g['projected_save_pct']:<7.3f} {g['projected_gaa']:<6.2f} "
            f"{g['projected_shutouts']:<5} {g['fantasy_points']:<7}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fantasy Hockey Projections - project NHL player stats for fantasy leagues"
    )
    parser.add_argument(
        "--live", action="store_true",
        help="Fetch live data from the NHL API (default: use sample data)"
    )
    parser.add_argument(
        "--regression", type=float, default=0.15,
        help="Regression weight toward league average (0-1, default: 0.15)"
    )
    parser.add_argument(
        "--top", type=int, default=25,
        help="Number of top players to display (default: 25)"
    )
    parser.add_argument(
        "--skaters-only", action="store_true",
        help="Only show skater projections"
    )
    parser.add_argument(
        "--goalies-only", action="store_true",
        help="Only show goalie projections"
    )
    args = parser.parse_args()

    show_skaters = not args.goalies_only
    show_goalies = not args.skaters_only

    if args.live:
        print("Fetching live NHL stats...")
        try:
            skaters = get_skater_stats() if show_skaters else []
            goalies = get_goalie_stats() if show_goalies else []
        except Exception as e:
            print(f"Error fetching live data: {e}", file=sys.stderr)
            print("Falling back to sample data.", file=sys.stderr)
            skaters = build_sample_skaters() if show_skaters else []
            goalies = build_sample_goalies() if show_goalies else []
    else:
        skaters = build_sample_skaters() if show_skaters else []
        goalies = build_sample_goalies() if show_goalies else []

    if show_skaters and skaters:
        projected_skaters = project_all_skaters(skaters, args.regression)
        ranked = rank_skaters(projected_skaters)
        print("\n=== Fantasy Hockey Skater Projections ===\n")
        print(format_skater_table(ranked, args.top))

    if show_goalies and goalies:
        projected_goalies = project_all_goalies(goalies, args.regression)
        ranked = rank_goalies(projected_goalies)
        print("\n=== Fantasy Hockey Goalie Projections ===\n")
        print(format_goalie_table(ranked, args.top))

    print()


if __name__ == "__main__":
    main()
