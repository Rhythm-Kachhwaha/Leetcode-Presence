const LOCAL_API = "http://127.0.0.1:8000";
const PROBLEM_URL = /^https:\/\/leetcode\.com\/problems\/([^/?#]+)/;

let lastTrackedSlug = undefined;

function getProblemSlug(url) {
  return PROBLEM_URL.exec(url || "")?.[1] ?? null;
}

async function post(endpoint) {
  const response = await fetch(`${LOCAL_API}${endpoint}`, { method: "POST" });
  const body = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(body.detail || `Local API returned ${response.status}`);
  }

  return body;
}

async function trackSlug(slug) {
  if (slug === lastTrackedSlug) {
    return;
  }

  lastTrackedSlug = slug;
  try {
    if (slug) {
      await post(`/activity/from-problem/${encodeURIComponent(slug)}`);
      console.info(`LeetPresence is tracking: ${slug}`);
    } else {
      await post("/activity/clear");
      console.info("LeetPresence cleared the current problem.");
    }
  } catch (error) {
    lastTrackedSlug = undefined;
    console.error("LeetPresence:", error.message);
  }
}

async function syncActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  await trackSlug(getProblemSlug(tab?.url));
}

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "PROBLEM_OPENED" && typeof message.slug === "string") {
    trackSlug(message.slug);
  }
});

chrome.tabs.onActivated.addListener(syncActiveTab);
chrome.tabs.onUpdated.addListener((_tabId, changeInfo, tab) => {
  if (tab.active && changeInfo.url) {
    syncActiveTab();
  }
});
chrome.runtime.onInstalled.addListener(syncActiveTab);
chrome.runtime.onStartup.addListener(syncActiveTab);
