let lastReportedSlug = null;

function getProblemSlug() {
  const match = window.location.pathname.match(/^\/problems\/([^/]+)/);
  return match ? match[1] : null;
}

function reportCurrentProblem() {
  const slug = getProblemSlug();

  if (!slug || slug === lastReportedSlug) {
    return;
  }

  lastReportedSlug = slug;
  chrome.runtime.sendMessage({ type: "PROBLEM_OPENED", slug }, (response) => {
    if (chrome.runtime.lastError) {
      console.error("LeetPresence:", chrome.runtime.lastError.message);
      return;
    }

    if (!response?.ok) {
      console.error("LeetPresence could not save the problem:", response?.error);
      lastReportedSlug = null;
      return;
    }

    console.info(`LeetPresence is tracking: ${slug}`);
  });
}

reportCurrentProblem();

// LeetCode navigates between problems without always reloading the page.
setInterval(reportCurrentProblem, 1000);
