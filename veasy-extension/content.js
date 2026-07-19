// content.js
// Runs on every page (see manifest.json "matches"). Detects a text
// selection, shows a small "Explain" button near it, and on click opens
// a popup panel that (for now) talks to a MOCKED background script.
// Swap the mock in background.js for a real backend call when ready.

(function () {
  const BUTTON_ID = 'veasy-trigger-btn';
  const PANEL_ID = 'veasy-panel';
  const MIN_SELECTION_LENGTH = 12;

  let currentButton = null;
  let currentPanel = null;

  function removeButton() {
    if (currentButton) {
      currentButton.remove();
      currentButton = null;
    }
  }

  function removePanel() {
    if (currentPanel) {
      currentPanel.remove();
      currentPanel = null;
    }
  }

  function getSelectionRect() {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return null;
    const range = selection.getRangeAt(0);
    const rects = range.getClientRects();
    if (rects.length === 0) return null;
    return rects[rects.length - 1]; // anchor near the end of the selection
  }

  function showButton(rect, selectedText) {
    removeButton();
    const btn = document.createElement('button');
    btn.id = BUTTON_ID;
    btn.textContent = '\u25B6 Explain';
    btn.style.top = `${window.scrollY + rect.bottom + 6}px`;
    btn.style.left = `${window.scrollX + rect.left}px`;

    // Prevent the button click from collapsing the text selection first.
    btn.addEventListener('mousedown', (e) => {
      e.preventDefault();
      e.stopPropagation();
    });

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      openPanel(rect, selectedText);
      removeButton();
    });

    document.body.appendChild(btn);
    currentButton = btn;
  }

  function openPanel(rect, selectedText) {
    removePanel();

    const panel = document.createElement('div');
    panel.id = PANEL_ID;
    panel.style.top = `${window.scrollY + rect.bottom + 6}px`;
    panel.style.left = `${window.scrollX + rect.left}px`;

    panel.innerHTML = `
      <div class="veasy-panel-header">
        <span>Veasy</span>
        <button class="veasy-close-btn" aria-label="Close">\u2715</button>
      </div>
      <div class="veasy-panel-body">
        <div class="veasy-loading">Finding the best explanation\u2026</div>
      </div>
    `;

    panel.querySelector('.veasy-close-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      removePanel();
    });

    document.body.appendChild(panel);
    currentPanel = panel;

    requestExplanation(selectedText)
      .then((result) => renderResult(panel, result))
      .catch((err) => renderError(panel, err));
  }

  function renderResult(panel, result) {
    const body = panel.querySelector('.veasy-panel-body');
    if (result.type === 'video') {
      body.innerHTML = `
        <div class="veasy-concept-name">${escapeHtml(result.concept)}</div>
        <video controls autoplay muted src="${result.videoUrl}" class="veasy-video"></video>
      `;
    } else {
      body.innerHTML = `
        <div class="veasy-concept-name">${escapeHtml(result.concept || 'Quick explanation')}</div>
        <p class="veasy-text-fallback">${escapeHtml(result.text)}</p>
      `;
    }
  }

  function renderError(panel, err) {
    const body = panel.querySelector('.veasy-panel-body');
    body.innerHTML = `<p class="veasy-error">Couldn't load an explanation right now.</p>`;
    console.error('[Veasy]', err);
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Sends the highlighted text to the background service worker. Today
  // background.js mocks the response so you can see the whole UI flow
  // work end-to-end before any backend exists. Later, background.js
  // will fetch() your real API instead.
  function requestExplanation(text) {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage(
        { type: 'VEASY_GET_EXPLANATION', text },
        (response) => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError);
            return;
          }
          if (!response || response.error) {
            reject(response ? response.error : 'Unknown error');
            return;
          }
          resolve(response.result);
        }
      );
    });
  }

  document.addEventListener('mouseup', (e) => {
    if (e.target.closest(`#${BUTTON_ID}, #${PANEL_ID}`)) return;

    removeButton();

    const selection = window.getSelection();
    const text = selection ? selection.toString().trim() : '';

    if (text.length < MIN_SELECTION_LENGTH) return;

    const rect = getSelectionRect();
    if (!rect) return;

    showButton(rect, text);
  });

  document.addEventListener('mousedown', (e) => {
    if (e.target.closest(`#${BUTTON_ID}, #${PANEL_ID}`)) return;
    removeButton();
    removePanel();
  });

  // Keep the MVP simple: dismiss the button on scroll rather than
  // repositioning it. Repositioning-on-scroll is a nice v2 improvement.
  window.addEventListener('scroll', () => {
    removeButton();
  }, { passive: true });
})();
