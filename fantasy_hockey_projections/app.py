"""Flask web application for fantasy hockey projections."""

import json

from flask import Flask, jsonify, render_template, request

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

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/projections")
def api_projections():
    """Return projected and ranked player data as JSON.

    Query params:
        source: "live" or "sample" (default: "sample")
        regression: float 0-1 (default: 0.15)
        position: "all", "skaters", "goalies" (default: "all")
    """
    source = request.args.get("source", "sample")
    regression = float(request.args.get("regression", 0.15))
    position = request.args.get("position", "all")

    regression = max(0.0, min(1.0, regression))

    skaters_data = []
    goalies_data = []

    if position in ("all", "skaters"):
        if source == "live":
            try:
                raw_skaters = get_skater_stats()
            except Exception:
                raw_skaters = build_sample_skaters()
        else:
            raw_skaters = build_sample_skaters()

        projected = project_all_skaters(raw_skaters, regression)
        skaters_data = rank_skaters(projected)

    if position in ("all", "goalies"):
        if source == "live":
            try:
                raw_goalies = get_goalie_stats()
            except Exception:
                raw_goalies = build_sample_goalies()
        else:
            raw_goalies = build_sample_goalies()

        projected = project_all_goalies(goalies=raw_goalies, regression_weight=regression)
        goalies_data = rank_goalies(projected)

    return jsonify({
        "skaters": skaters_data,
        "goalies": goalies_data,
        "settings": {
            "source": source,
            "regression": regression,
            "position": position,
        },
    })


def main():
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
