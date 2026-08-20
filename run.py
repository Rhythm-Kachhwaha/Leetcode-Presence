"""Start the local API and Discord Rich Presence updater together."""

from threading import Thread

import uvicorn

from presence import run_presence


if __name__ == "__main__":
    Thread(target=run_presence, daemon=True).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
