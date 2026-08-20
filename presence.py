"""Publish LeetCode progress to the locally running Discord desktop client."""

import time

from pypresence import Presence

from config import (
    DISCORD_APPLICATION_ID,
    LEETCODE_USERNAME,
    REFRESH_SECONDS,
    RICH_PRESENCE_ASSET_KEY,
    DIFFICULTY_ASSET_KEYS,
)
from database import Base, SessionLocal, engine
from leetcode import fetch_profile_stats
from models import CurrentActivityModel


Base.metadata.create_all(bind=engine)
DIFFICULTY_INDICATORS = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}


def get_current_problem() -> CurrentActivityModel | None:
    with SessionLocal() as db:
        return db.get(CurrentActivityModel, 1)


def presence_payload() -> dict:
    total_solved, streak = fetch_profile_stats(LEETCODE_USERNAME)
    current_problem = get_current_problem()

    if current_problem is None:
        details = "LeetCode progress"
    else:
        indicator = DIFFICULTY_INDICATORS.get(current_problem.difficulty, "💻")
        details = f"{indicator} {current_problem.difficulty} • {current_problem.title}"

    payload = {
        "details": details,
        "state": f"{total_solved} solved • 🔥 {streak}-day streak",
        "buttons": [
            {
                "label": "View LeetCode Profile",
                "url": f"https://leetcode.com/{LEETCODE_USERNAME}/",
            }
        ],
    }

    asset_key = RICH_PRESENCE_ASSET_KEY
    if current_problem is not None:
        asset_key = DIFFICULTY_ASSET_KEYS.get(current_problem.difficulty, asset_key)

    if asset_key:
        payload["large_image"] = asset_key
        payload["large_text"] = "LeetPresence"

    return payload


def run_presence() -> None:
    rpc = None
    print("LeetPresence started. Press Ctrl+C to stop it.")

    while True:
        try:
            if rpc is None:
                rpc = Presence(DISCORD_APPLICATION_ID)
                rpc.connect()
                print("Connected to Discord.")

            payload = presence_payload()
            rpc.update(**payload)
            print(f"Updated Discord presence: {payload['details']}")
        except Exception as error:
            print(f"Presence update failed; retrying in {REFRESH_SECONDS}s: {error}")
            rpc = None

        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    run_presence()
