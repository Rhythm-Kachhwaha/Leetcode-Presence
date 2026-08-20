import os


DISCORD_APPLICATION_ID = os.getenv(
    "LEETPRESENCE_DISCORD_APPLICATION_ID", "1540047328013066401"
)
LEETCODE_USERNAME = os.getenv("LEETPRESENCE_LEETCODE_USERNAME", "RhythmKachhwaha")
REFRESH_SECONDS = int(os.getenv("LEETPRESENCE_REFRESH_SECONDS", "60"))

# Upload assets/leetpresence.png to Discord with this asset key.
RICH_PRESENCE_ASSET_KEY = os.getenv("LEETPRESENCE_ASSET_KEY", "leetpresence")
DIFFICULTY_ASSET_KEYS = {
    "Easy": os.getenv("LEETPRESENCE_EASY_ASSET_KEY", "easy"),
    "Medium": os.getenv("LEETPRESENCE_MEDIUM_ASSET_KEY", "medium"),
    "Hard": os.getenv("LEETPRESENCE_HARD_ASSET_KEY", "hard"),
}
