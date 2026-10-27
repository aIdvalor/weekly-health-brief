#!/usr/bin/env python3
"""Regenerate synthetic sample_data/ + charts/ (optional). Requires matplotlib."""
from __future__ import annotations

import csv
import random
import shutil
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAMPLE = ROOT / "sample_data"
CHARTS = ROOT / "charts"
BRIEF_CHARTS = ROOT / "brief" / "charts"

START = date(2025, 3, 1)
DAYS = 42
random.seed(42)


def main() -> None:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError as e:
        raise SystemExit("matplotlib required: pip install matplotlib") from e

    SAMPLE.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)

    daily_rows = []
    tennis_rows = []
    for i in range(DAYS):
        d = START + timedelta(days=i)
        base_sleep = 7.1 + 0.35 * ((i % 7) / 6)
        sleep_h = 5.8 if d == date(2025, 4, 8) else base_sleep + random.uniform(-0.35, 0.45)
        in_featured = date(2025, 4, 5) <= d <= date(2025, 4, 11)
        steps_base = 7800 if not in_featured else 9800
        steps = int(steps_base + random.uniform(-1800, 2200))
        rhr = max(52.0, round(56 + random.uniform(-2.5, 3.0), 1))
        daily_rows.append(
            {
                "date": d.isoformat(),
                "steps": steps,
                "steps_goal": 8000,
                "avg_rhr": rhr,
                "sleep_total_min": round(sleep_h * 60),
                "calories": int(2100 + random.uniform(-200, 400)),
            }
        )
        weekday = d.weekday()
        play = (
            weekday in (0, 1, 3, 4, 5)
            if in_featured
            else weekday in (1, 4) or (weekday == 6 and (i // 7) % 2 == 0)
        )
        if play:
            dur = random.choice([55, 70, 85, 95, 110])
            tennis_rows.append(
                {
                    "date": d.isoformat(),
                    "duration_min": float(dur),
                    "train_load": float(round(dur * random.uniform(1.05, 1.35), 0)),
                    "calories": float(int(dur * 8.5)),
                    "category": "tennis",
                }
            )

    with (SAMPLE / "daily_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["date", "steps", "steps_goal", "avg_rhr", "sleep_total_min", "calories"]
        )
        w.writeheader()
        w.writerows(daily_rows)
    with (SAMPLE / "workouts_tennis.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["date", "duration_min", "train_load", "calories", "category"]
        )
        w.writeheader()
        w.writerows(tennis_rows)

    plt.style.use("dark_background")
    dates = [date.fromisoformat(r["date"]) for r in daily_rows]
    steps = [r["steps"] for r in daily_rows]
    sleep_h = [r["sleep_total_min"] / 60 for r in daily_rows]
    rhr = [r["avg_rhr"] for r in daily_rows]

    def style_ax(ax, title):
        ax.set_title(title, fontsize=12, pad=10)
        ax.grid(True, alpha=0.25)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)

    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=140)
    ax.plot(dates, sleep_h, color="#5eb1ff", linewidth=1.8)
    ax.axhspan(7, 9, color="#7ddea2", alpha=0.12)
    ax.set_ylabel("Hours")
    style_ax(ax, "SAMPLE · Sleep (hours)")
    fig.tight_layout()
    fig.savefig(CHARTS / "sleep.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=140)
    ax.plot(dates, steps, color="#7ddea2", linewidth=1.8)
    ax.axhline(8000, color="#f0b429", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_ylabel("Steps")
    style_ax(ax, "SAMPLE · Daily steps")
    fig.tight_layout()
    fig.savefig(CHARTS / "steps.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=140)
    ax.plot(dates, rhr, color="#ff8a7a", linewidth=1.8)
    ax.set_ylabel("bpm")
    style_ax(ax, "SAMPLE · Resting heart rate")
    fig.tight_layout()
    fig.savefig(CHARTS / "resting_hr.png")
    plt.close()

    week_load: dict[date, float] = defaultdict(float)
    for t in tennis_rows:
        td = date.fromisoformat(t["date"])
        ws = td - timedelta(days=td.weekday())
        week_load[ws] += t["train_load"]
    wks = sorted(week_load)
    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=140)
    ax.bar([w.isoformat() for w in wks], [week_load[w] for w in wks], color="#5eb1ff", width=0.6)
    ax.set_ylabel("Train load")
    ax.set_title("SAMPLE · Weekly tennis load", fontsize=12, pad=10)
    ax.grid(True, axis="y", alpha=0.25)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig(CHARTS / "tennis_load.png")
    plt.close()

    BRIEF_CHARTS.mkdir(parents=True, exist_ok=True)
    for name in ("sleep.png", "steps.png", "resting_hr.png", "tennis_load.png"):
        shutil.copy(CHARTS / name, BRIEF_CHARTS / name)
    print(f"Wrote sample_data + charts ({len(daily_rows)} days, {len(tennis_rows)} tennis sessions)")


if __name__ == "__main__":
    main()
