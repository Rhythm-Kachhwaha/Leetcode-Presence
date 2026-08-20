# LeetPresence Brave extension

This local extension notices the LeetCode problem open in Brave and sends its
slug to the local LeetPresence API.

## Install in Brave

1. Start the API: `python -m uvicorn main:app --reload`
2. Open `brave://extensions`.
3. Enable **Developer mode**.
4. Select **Load unpacked**.
5. Choose this `browser-extension` folder.

Keep `presence.py` and the FastAPI server running. Open any URL in the form
`https://leetcode.com/problems/<problem-slug>/`; the extension calls the local
API, and Discord Rich Presence refreshes within one minute.

The extension can access only LeetCode pages and the local API at
`127.0.0.1:8000`.
