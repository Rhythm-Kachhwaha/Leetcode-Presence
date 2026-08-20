const LOCAL_API = "http://127.0.0.1:8000";

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type !== "PROBLEM_OPENED" || typeof message.slug !== "string") {
    return;
  }

  const endpoint = `${LOCAL_API}/activity/from-problem/${encodeURIComponent(message.slug)}`;

  fetch(endpoint, { method: "POST" })
    .then(async (response) => {
      const body = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(body.detail || `Local API returned ${response.status}`);
      }

      sendResponse({ ok: true, activity: body });
    })
    .catch((error) => {
      sendResponse({ ok: false, error: error.message });
    });

  return true;
});
