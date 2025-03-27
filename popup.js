// Get the button element
const toggleButton = document.getElementById('toggleButton');

// Load the current state of the ad blocker from storage
chrome.storage.local.get('isEnabled', (data) => {
  const isEnabled = data.isEnabled !== false;
  updateButtonState(isEnabled);
});

// Listen for changes to the button click
toggleButton.addEventListener('click', () => {
  // Toggle the state
  const newState = toggleButton.classList.contains('disabled') ? true : false;
  chrome.storage.local.set({ isEnabled: newState }, () => {
    updateButtonState(newState);
    // After the state is set, reload the current tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.reload(tabs[0].id); // Reload the active tab
    });
  });
});

// Function to update the button text and color based on the state
function updateButtonState(isEnabled) {
  if (isEnabled) {
    toggleButton.textContent = 'Disable Ad Blocker';
    toggleButton.classList.remove('disabled');
  } else {
    toggleButton.textContent = 'Enable Ad Blocker';
    toggleButton.classList.add('disabled');
  }
}
