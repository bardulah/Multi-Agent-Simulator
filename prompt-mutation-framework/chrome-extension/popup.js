/**
 * Popup UI Logic for Marketplace Description Generator
 */

// DOM Elements
const apiKeyInput = document.getElementById('api-key');
const saveApiKeyBtn = document.getElementById('save-api-key');
const apiKeyStatus = document.getElementById('api-key-status');
const platformInput = document.getElementById('platform');
const itemTitleInput = document.getElementById('item-title');
const conditionSelect = document.getElementById('condition');
const priceInput = document.getElementById('price');
const defectsInput = document.getElementById('defects');
const generateBtn = document.getElementById('generate-btn');
const resultsSection = document.getElementById('results-section');
const statusMessage = document.getElementById('status-message');
const generationTime = document.getElementById('generation-time');

// Result elements
const variantATextarea = document.getElementById('variant-a');
const variantBTextarea = document.getElementById('variant-b');
const variantCTextarea = document.getElementById('variant-c');
const charCountA = document.getElementById('char-count-a');
const charCountB = document.getElementById('char-count-b');
const charCountC = document.getElementById('char-count-c');
const riskScoreSpan = document.getElementById('risk-score');
const modulesSpan = document.getElementById('modules');
const charBudgetSpan = document.getElementById('char-budget');
const warningsDiv = document.getElementById('warnings');

// Load saved API key and detect platform on popup load
document.addEventListener('DOMContentLoaded', async () => {
    // Load API key from storage
    const { apiKey } = await chrome.storage.local.get(['apiKey']);
    if (apiKey) {
        apiKeyInput.value = apiKey;
        apiKeyStatus.textContent = '✅ Saved';
        apiKeyStatus.className = 'status success';
    }

    // Detect current platform
    detectPlatform();
});

// Save API Key
saveApiKeyBtn.addEventListener('click', async () => {
    const apiKey = apiKeyInput.value.trim();

    if (!apiKey) {
        showStatus(apiKeyStatus, '❌ Empty', 'error');
        return;
    }

    if (!apiKey.startsWith('sk-ant-')) {
        showStatus(apiKeyStatus, '⚠️ Invalid format', 'error');
        return;
    }

    await chrome.storage.local.set({ apiKey });
    showStatus(apiKeyStatus, '✅ Saved', 'success');
});

// Detect Platform
async function detectPlatform() {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (!tab || !tab.url) {
            platformInput.value = 'Not on marketplace page';
            return;
        }

        const url = tab.url.toLowerCase();

        if (url.includes('ebay.de')) {
            platformInput.value = 'eBay.de';
        } else if (url.includes('ebay.com')) {
            platformInput.value = 'eBay.com';
        } else if (url.includes('vinted.de')) {
            platformInput.value = 'Vinted.de';
        } else if (url.includes('vinted.fr')) {
            platformInput.value = 'Vinted.fr';
        } else if (url.includes('kleinanzeigen.de')) {
            platformInput.value = 'Kleinanzeigen';
        } else {
            platformInput.value = 'Unknown (manual mode)';
        }
    } catch (error) {
        console.error('Platform detection error:', error);
        platformInput.value = 'Error detecting platform';
    }
}

// Generate Descriptions
generateBtn.addEventListener('click', async () => {
    const apiKey = apiKeyInput.value.trim();
    const itemTitle = itemTitleInput.value.trim();
    const condition = conditionSelect.value;
    const price = parseFloat(priceInput.value);
    const defects = defectsInput.value.trim().split(',').map(d => d.trim()).filter(d => d);

    // Validation
    if (!apiKey) {
        showGlobalStatus('❌ Please save API key first', 'error');
        return;
    }

    if (!itemTitle) {
        showGlobalStatus('❌ Please enter item title', 'error');
        return;
    }

    if (!price || price <= 0) {
        showGlobalStatus('❌ Please enter valid price', 'error');
        return;
    }

    // Start generation
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating... ⏳';
    showGlobalStatus('Generating descriptions...', 'info');

    const startTime = Date.now();

    try {
        // Call background script to generate
        const response = await chrome.runtime.sendMessage({
            type: 'GENERATE_DESCRIPTION',
            data: {
                apiKey,
                itemTitle,
                condition,
                price,
                defects,
                platform: platformInput.value
            }
        });

        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

        if (response.success) {
            displayResults(response.result);
            showGlobalStatus('✅ Generated successfully!', 'success');
            generationTime.textContent = `(${elapsed}s)`;
        } else {
            throw new Error(response.error || 'Generation failed');
        }

    } catch (error) {
        console.error('Generation error:', error);
        showGlobalStatus(`❌ Error: ${error.message}`, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Descriptions ✨';
    }
});

// Display Results
function displayResults(result) {
    // Show results section
    resultsSection.classList.remove('hidden');

    // Populate variants
    variantATextarea.value = result.variant_a_emotion.text;
    variantBTextarea.value = result.variant_b_value.text;
    variantCTextarea.value = result.variant_c_trust.text;

    // Character counts
    charCountA.textContent = `${result.variant_a_emotion.char_count} chars`;
    charCountB.textContent = `${result.variant_b_value.char_count} chars`;
    charCountC.textContent = `${result.variant_c_trust.char_count} chars`;

    // Metadata
    const metadata = result.metadata;
    riskScoreSpan.textContent = `${metadata.risk_score}/100 (${metadata.risk_level})`;
    riskScoreSpan.className = `risk-${metadata.risk_level.toLowerCase()}`;

    modulesSpan.textContent = metadata.modules_applied.join(', ') || 'Base';
    charBudgetSpan.textContent = `${metadata.character_budget} chars`;

    // Warnings
    if (metadata.safety_warnings && metadata.safety_warnings.length > 0) {
        warningsDiv.innerHTML = metadata.safety_warnings.map(w => `<div class="warning">${w}</div>`).join('');
        warningsDiv.style.display = 'block';
    } else {
        warningsDiv.style.display = 'none';
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Copy to Clipboard
document.querySelectorAll('.btn-copy').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const targetId = e.target.dataset.target;
        const textarea = document.getElementById(targetId);
        const text = textarea.value;

        try {
            await navigator.clipboard.writeText(text);
            e.target.textContent = '✅ Copied!';
            setTimeout(() => {
                e.target.textContent = '📋 Copy';
            }, 2000);
        } catch (error) {
            console.error('Copy failed:', error);
            e.target.textContent = '❌ Failed';
        }
    });
});

// Insert to Page
document.querySelectorAll('.btn-insert').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const targetId = e.target.dataset.target;
        const textarea = document.getElementById(targetId);
        const text = textarea.value;

        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

            await chrome.tabs.sendMessage(tab.id, {
                type: 'INSERT_DESCRIPTION',
                text: text
            });

            e.target.textContent = '✅ Inserted!';
            setTimeout(() => {
                e.target.textContent = '📝 Insert to Page';
            }, 2000);
        } catch (error) {
            console.error('Insert failed:', error);
            e.target.textContent = '❌ Failed';
        }
    });
});

// Helper: Show status message
function showGlobalStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-${type}`;
}

function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status ${type}`;
}
