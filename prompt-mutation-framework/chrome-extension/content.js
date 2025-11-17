/**
 * Content Script
 * Handles DOM manipulation on marketplace pages
 */

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'INSERT_DESCRIPTION') {
        const success = insertDescription(message.text);
        sendResponse({ success });
    }
});

/**
 * Insert generated description into marketplace form
 */
function insertDescription(text) {
    const url = window.location.href.toLowerCase();

    try {
        if (url.includes('ebay.de') || url.includes('ebay.com')) {
            return insertEbayDescription(text);
        } else if (url.includes('vinted')) {
            return insertVintedDescription(text);
        } else if (url.includes('kleinanzeigen')) {
            return insertKleinanzeigenDescription(text);
        } else {
            console.warn('Unknown platform for insertion');
            return false;
        }
    } catch (error) {
        console.error('Description insertion failed:', error);
        return false;
    }
}

/**
 * Insert into eBay listing form
 */
function insertEbayDescription(text) {
    // eBay description textarea selectors (may vary)
    const selectors = [
        'textarea[name="description"]',
        'textarea[id*="description"]',
        'textarea[placeholder*="description"]',
        '.description textarea',
        '#description'
    ];

    for (const selector of selectors) {
        const textarea = document.querySelector(selector);
        if (textarea) {
            textarea.value = text;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            textarea.dispatchEvent(new Event('change', { bubbles: true }));

            // Highlight briefly
            highlightElement(textarea);

            console.log('✅ Inserted into eBay description field');
            return true;
        }
    }

    console.warn('⚠️ eBay description field not found');
    return false;
}

/**
 * Insert into Vinted listing form
 */
function insertVintedDescription(text) {
    // Vinted description textarea selectors
    const selectors = [
        'textarea[name="description"]',
        'textarea[id*="description"]',
        'textarea[placeholder*="Describe"]',
        '.description textarea'
    ];

    for (const selector of selectors) {
        const textarea = document.querySelector(selector);
        if (textarea) {
            textarea.value = text;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            textarea.dispatchEvent(new Event('change', { bubbles: true }));

            highlightElement(textarea);

            console.log('✅ Inserted into Vinted description field');
            return true;
        }
    }

    console.warn('⚠️ Vinted description field not found');
    return false;
}

/**
 * Insert into Kleinanzeigen listing form
 */
function insertKleinanzeigenDescription(text) {
    // Kleinanzeigen description textarea selectors
    const selectors = [
        'textarea[name="description"]',
        'textarea[id="postad-description"]',
        'textarea[placeholder*="Beschreibung"]',
        '#description'
    ];

    for (const selector of selectors) {
        const textarea = document.querySelector(selector);
        if (textarea) {
            textarea.value = text;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            textarea.dispatchEvent(new Event('change', { bubbles: true }));

            highlightElement(textarea);

            console.log('✅ Inserted into Kleinanzeigen description field');
            return true;
        }
    }

    console.warn('⚠️ Kleinanzeigen description field not found');
    return false;
}

/**
 * Highlight element briefly
 */
function highlightElement(element) {
    const originalBorder = element.style.border;
    const originalBoxShadow = element.style.boxShadow;

    element.style.border = '2px solid #10b981';
    element.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.5)';

    setTimeout(() => {
        element.style.border = originalBorder;
        element.style.boxShadow = originalBoxShadow;
    }, 2000);
}

/**
 * Add helper button to marketplace forms (optional enhancement)
 */
function addGeneratorButton() {
    const url = window.location.href.toLowerCase();

    // Only add on listing creation pages
    if (!url.includes('/sell') && !url.includes('/new') && !url.includes('/aufgeben')) {
        return;
    }

    // Check if button already exists
    if (document.getElementById('marketplace-generator-btn')) {
        return;
    }

    // Find description field
    const textarea = findDescriptionField();
    if (!textarea) {
        return;
    }

    // Create button
    const button = document.createElement('button');
    button.id = 'marketplace-generator-btn';
    button.className = 'marketplace-generator-helper-btn';
    button.textContent = '✨ Generate Description';
    button.type = 'button';

    button.addEventListener('click', () => {
        // Open extension popup (programmatic popup not possible, show notification instead)
        showNotification('Click the extension icon in the toolbar to generate descriptions!');
    });

    // Insert button near textarea
    textarea.parentElement.insertBefore(button, textarea.nextSibling);
}

/**
 * Find description field on page
 */
function findDescriptionField() {
    const selectors = [
        'textarea[name="description"]',
        'textarea[id*="description"]',
        'textarea[placeholder*="description"]',
        'textarea[placeholder*="Describe"]',
        'textarea[placeholder*="Beschreibung"]',
        '.description textarea',
        '#description'
    ];

    for (const selector of selectors) {
        const el = document.querySelector(selector);
        if (el) return el;
    }

    return null;
}

/**
 * Show notification overlay
 */
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'marketplace-generator-notification';
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize on page load
window.addEventListener('load', () => {
    addGeneratorButton();
});

console.log('Marketplace Description Generator - Content Script Loaded');
