from datetime import datetime

import requests


LEETCODE_URL = "https://leetcode.com/graphql"


def fetch_problem(slug: str) -> dict | None:
    query = """
    query problemBySlug($slug: String!) {
        question(titleSlug: $slug) {
            questionFrontendId
            title
            difficulty
            titleSlug
        }
    }
    """
    response = requests.post(
        LEETCODE_URL,
        json={"query": query, "variables": {"slug": slug}},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()

    if payload.get("errors"):
        raise ValueError(payload["errors"][0].get("message", "LeetCode request failed"))

    return payload.get("data", {}).get("question")


def fetch_profile_stats(username: str) -> tuple[int, int]:
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
            "variables": {"username": username, "year": datetime.now().year},
        },
        timeout=15,
    )
    response.raise_for_status()
    user = response.json().get("data", {}).get("matchedUser")

    if user is None:
        raise ValueError(f"LeetCode user '{username}' was not found.")

    solved = next(
        item["count"]
        for item in user["submitStats"]["acSubmissionNum"]
        if item["difficulty"] == "All"
    )
    return solved, user["userCalendar"]["streak"]
