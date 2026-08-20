"""Publish LeetCode progress to the locally running Discord desktop client."""

import sqlite3
import time
from datetime import datetime
from pathlib import Path

import requests
from pypresence import Presence


DISCORD_APPLICATION_ID = "1540047328013066401"
LEETCODE_USERNAME = "RhythmKachhwaha"
DATABASE_PATH = Path(__file__).with_name("leetpresence.db")
REFRESH_SECONDS = 60
LEETCODE_URL = "https://leetcode.com/graphql"


def get_leetcode_stats() -> tuple[int, int]:
    query = """
    query userProgress($username: String!, $year: Int!) {
        matchedUser(username: $username) {
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
            userCalendar(year: $year) {
                streak
            }
        }
    }
    """
    response = requests.post(
        LEETCODE_URL,
        json={
            "query": query,
            "variables": {
                "username": LEETCODE_USERNAME,
                "year": datetime.now().year,
            },
        },
        timeout=15,
    )
    response.raise_for_status()

    user = response.json()["data"]["matchedUser"]
    if user is None:
        raise ValueError(f"LeetCode user '{LEETCODE_USERNAME}' was not found.")

    solved = next(
        item["count"]
        for item in user["submitStats"]["acSubmissionNum"]
        if item["difficulty"] == "All"
    )
    return solved, user["userCalendar"]["streak"]


def get_current_problem() -> tuple[str, str] | None:
    if not DATABASE_PATH.exists():
        return None

    with sqlite3.connect(DATABASE_PATH) as connection:
        row = connection.execute(
            "SELECT title, difficulty FROM activity ORDER BY id DESC LIMIT 1"
        ).fetchone()

    return tuple(row) if row else None


def update_presence(rpc: Presence) -> None:
    total_solved, streak = get_leetcode_stats()
    current_problem = get_current_problem()

    if current_problem:
        title, difficulty = current_problem
        details = f"Solving: {title} ({difficulty})"
    else:
        details = "Practicing LeetCode"

    rpc.update(
        details=details,
        state=f"{total_solved} solved • {streak}-day streak",
        buttons=[
            {
                "label": "View LeetCode Profile",
                "url": f"https://leetcode.com/{LEETCODE_USERNAME}/",
            }
        ],
    )
    print(f"Updated Discord presence: {details}")


def main() -> None:
    rpc = Presence(DISCORD_APPLICATION_ID)
    rpc.connect()
    print("Connected to Discord. Press Ctrl+C to stop LeetPresence.")

    while True:
        try:
            update_presence(rpc)
        except Exception as error:
            print(f"Presence update failed: {error}")
        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()
