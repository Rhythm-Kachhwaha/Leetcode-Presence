# LeetPresence

Show your active LeetCode problem, total solved count, and current streak as
Discord Rich Presence. A local Brave extension detects the problem page you
open and sends only its slug to the local API.

## Quick start

1. Install Python 3.9+ and Discord Desktop.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. In the Discord Developer Portal, open your application, go to **Rich
   Presence → Art Assets**, and upload the contents of [assets](assets) with
   the matching asset keys: `leetpresence`, `easy`, `medium`, and `hard`.
4. In Brave, open `brave://extensions`, enable **Developer mode**, choose
   **Load unpacked**, and select [browser-extension](browser-extension).
5. Start the app:

   ```powershell
   python run.py
   ```

   On Windows, you can also double-click `start_leetpresence.bat`.

6. Open a LeetCode problem. Discord refreshes within one minute.

## Customization

Set these environment variables before running the app when you want to use a
different Discord application or LeetCode account:

- `LEETPRESENCE_DISCORD_APPLICATION_ID`
- `LEETPRESENCE_LEETCODE_USERNAME`
- `LEETPRESENCE_REFRESH_SECONDS`
- `LEETPRESENCE_ASSET_KEY`
- `LEETPRESENCE_EASY_ASSET_KEY`
- `LEETPRESENCE_MEDIUM_ASSET_KEY`
- `LEETPRESENCE_HARD_ASSET_KEY`

The Rich Presence text and difficulty indicators live in `presence.py`.
