let isEnabled = true;

// List of all the rule resources by ID
const ruleIds = ['easylist_rules']; // Add more rule IDs as necessary

// Listen for changes to the extension's storage
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (changes.isEnabled) {
    isEnabled = changes.isEnabled.newValue;
    updateRules();
  }
});

// Update the rules based on whether the ad blocker is enabled or not
function updateRules() {
  const enableRuleIds = isEnabled ? ruleIds : [];
  const disableRuleIds = isEnabled ? [] : ruleIds;

  chrome.declarativeNetRequest.updateEnabledRulesets({
    enableRulesetIds: enableRuleIds,
    disableRulesetIds: disableRuleIds
  });
}

// Initialize rules state from storage
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get('isEnabled', (data) => {
    isEnabled = data.isEnabled !== undefined ? data.isEnabled : true;
    updateRules();
  });
});
