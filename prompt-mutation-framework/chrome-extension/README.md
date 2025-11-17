# Chrome Extension - Marketplace Description Generator

Browser extension that brings the **Prompt Mutation Framework** directly to marketplace listing pages.

---

## Features

✨ **One-Click Generation**: Generate 3 optimized description variants from extension popup
📝 **Auto-Insert**: Directly insert descriptions into marketplace forms (eBay, Vinted, Kleinanzeigen)
🔒 **Secure**: API key stored locally, never transmitted except to Anthropic
🎨 **Beautiful UI**: Clean, modern interface with gradient design
📊 **Metadata Display**: See risk scores, modules applied, character budgets
🌍 **Multi-Platform**: Works on eBay.de, eBay.com, Vinted, Kleinanzeigen

---

## Installation

### Option 1: Load Unpacked (Development)

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-repo/prompt-mutation-framework.git
   cd prompt-mutation-framework/chrome-extension
   ```

2. **Open Chrome Extensions**
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)

3. **Load Extension**
   - Click "Load unpacked"
   - Select the `chrome-extension` folder
   - Extension icon should appear in toolbar

4. **Configure API Key**
   - Click extension icon
   - Enter your Anthropic API key (starts with `sk-ant-`)
   - Click "Save"

### Option 2: Build for Production

```bash
# Package extension
cd chrome-extension
zip -r marketplace-generator-v1.0.zip . -x "*.git*" "README.md"

# Upload to Chrome Web Store
# https://chrome.google.com/webstore/devconsole
```

---

## Usage

### Quick Start

1. **Navigate to Marketplace**
   - Open eBay.de, Vinted, or Kleinanzeigen
   - Go to "Create Listing" or "Sell Item" page

2. **Open Extension**
   - Click extension icon in toolbar
   - Extension detects platform automatically

3. **Fill Form**
   - Item Title: "Apple iPhone 13 Pro 256GB"
   - Condition: "Excellent"
   - Price: 549
   - Defects (optional): "small screen scratch"

4. **Generate**
   - Click "Generate Descriptions ✨"
   - Wait 2-3 seconds

5. **Use Results**
   - Copy any of the 3 variants (Emotional, Value, Trust)
   - OR click "Insert to Page" to auto-fill marketplace form

---

## Architecture

### Files

```
chrome-extension/
├── manifest.json           # Extension configuration
├── popup.html              # Main UI
├── popup.js                # UI logic
├── popup-styles.css        # Popup styling
├── background.js           # API calls (service worker)
├── content.js              # DOM manipulation
├── content-styles.css      # Content script styling
├── icons/
│   ├── icon16.png          # Toolbar icon (16x16)
│   ├── icon48.png          # Extension page icon (48x48)
│   └── icon128.png         # Web Store icon (128x128)
└── README.md               # This file
```

### Components

**Popup (popup.html + popup.js)**:
- User interface for configuration and generation
- Collects item data from user input
- Displays 3 generated variants
- Shows metadata (risk score, modules, budget)

**Background (background.js)**:
- Service worker handling API calls
- Calls Anthropic API with Master Prompt
- Parses JSON response
- Returns variants + metadata

**Content Script (content.js)**:
- Runs on marketplace pages
- Detects description textarea fields
- Inserts generated text into forms
- Adds helper button (optional)

### Permissions

- `activeTab`: Detect current marketplace platform
- `storage`: Save API key locally
- `scripting`: Inject content scripts
- `host_permissions`: Access eBay, Vinted, Kleinanzeigen, Anthropic API

---

## Supported Platforms

| Platform | URL Pattern | Language | Status |
|----------|-------------|----------|--------|
| **eBay Deutschland** | `ebay.de/sl/sell*` | German | ✅ Supported |
| **eBay International** | `ebay.com/sl/sell*` | English | ✅ Supported |
| **Vinted DE** | `vinted.de/items/new*` | German | ✅ Supported |
| **Vinted FR** | `vinted.fr/items/new*` | French | ✅ Supported |
| **Kleinanzeigen** | `kleinanzeigen.de/p-anzeige-aufgeben*` | German | ✅ Supported |
| **Mercari EU** | N/A | English | ⏳ Planned |

### Adding New Platforms

Edit `manifest.json`:

```json
{
  "content_scripts": [
    {
      "matches": [
        "https://www.ebay.de/sl/sell*",
        "https://www.new-marketplace.com/create*"  // Add new pattern
      ],
      "js": ["content.js"],
      "css": ["content-styles.css"]
    }
  ]
}
```

Edit `content.js`:

```javascript
function insertDescription(text) {
    const url = window.location.href.toLowerCase();

    if (url.includes('new-marketplace.com')) {
        return insertNewMarketplaceDescription(text);
    }
    // ... existing platforms
}

function insertNewMarketplaceDescription(text) {
    const textarea = document.querySelector('textarea[name="item_description"]');
    if (textarea) {
        textarea.value = text;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        return true;
    }
    return false;
}
```

---

## API Key Security

### Best Practices

✅ **DO:**
- Store API key in `chrome.storage.local` (encrypted by browser)
- Only send API key to `api.anthropic.com` (HTTPS only)
- Clear API key on uninstall (optional: add uninstall listener)

❌ **DON'T:**
- Never commit API keys to Git
- Never log API keys to console
- Never send API keys to third-party servers

### Key Storage

API keys are stored using Chrome Storage API:

```javascript
// Save API key
await chrome.storage.local.set({ apiKey: 'sk-ant-xxx' });

// Retrieve API key
const { apiKey } = await chrome.storage.local.get(['apiKey']);

// Clear API key
await chrome.storage.local.remove('apiKey');
```

**Security Features:**
- Encrypted at rest by Chrome
- Only accessible to this extension
- Never synced to Chrome account (uses `local`, not `sync`)

---

## Troubleshooting

### Issue: Extension Not Loading

**Symptom**: Extension icon doesn't appear in toolbar

**Fix:**
1. Check Chrome version (Manifest v3 requires Chrome 88+)
2. Verify `manifest.json` syntax (use JSON validator)
3. Check Extensions page for errors (`chrome://extensions/`)

### Issue: API Key Not Saving

**Symptom**: "❌ Empty" or "⚠️ Invalid format" message

**Fix:**
- Ensure API key starts with `sk-ant-`
- Check for extra spaces or newlines
- Verify key is valid on Anthropic Console

### Issue: Generation Fails

**Symptom**: "❌ Error: API request failed" message

**Possible Causes:**
1. Invalid API key
2. Insufficient API credits
3. Network/firewall blocking `api.anthropic.com`
4. Rate limiting (too many requests)

**Debug Steps:**
```javascript
// Open popup → Right-click → Inspect → Console
// Check for error messages

// Open background service worker → Console
// chrome://extensions/ → Extension details → "Inspect views: service worker"
```

### Issue: Insert to Page Doesn't Work

**Symptom**: "Insert to Page" button does nothing

**Possible Causes:**
1. Not on supported marketplace page
2. Marketplace updated their HTML (selector changed)
3. Content script not injected

**Fix:**
```javascript
// Check if content script loaded
// Marketplace page → Right-click → Inspect → Console
// Should see: "Marketplace Description Generator - Content Script Loaded"

// If not loaded, check manifest.json URL patterns match current page
```

### Issue: Platform Not Detected

**Symptom**: "Detected Platform: Unknown (manual mode)"

**Fix:**
- Ensure you're on listing creation page (not homepage)
- Check URL matches patterns in `manifest.json`
- Reload extension and refresh marketplace page

---

## Performance

### Generation Time
- **Popup → API → Response**: 2-3 seconds
- Depends on: API latency, network speed, prompt complexity

### API Costs
- **~$0.01 per generation** (Claude Sonnet 4.5)
- Input tokens: ~2000 (Master Prompt + user data)
- Output tokens: ~300 (3 variants + metadata)

### Optimization Tips
- Use simulation mode for testing (no API calls)
- Cache common descriptions (future enhancement)
- Batch generate multiple listings (future enhancement)

---

## Customization

### Change Styling

Edit `popup-styles.css`:

```css
/* Change primary color */
header {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}

.btn-primary {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Adjust Popup Size

Edit `popup-styles.css`:

```css
body {
    width: 500px;  /* Default: 420px */
    min-height: 600px;  /* Default: 500px */
}
```

### Add Custom Platform

See "Adding New Platforms" section above.

---

## Future Enhancements (v2.0)

### Planned Features
- [ ] **Auto-Fill All Fields**: Detect item from page, pre-fill form automatically
- [ ] **Image Analysis**: Upload photos, extract item details via vision AI
- [ ] **Templates**: Save custom templates for frequently sold items
- [ ] **Bulk Mode**: Generate descriptions for CSV of items
- [ ] **Analytics**: Track which variants convert best
- [ ] **A/B Testing**: Automatically test variants, show results
- [ ] **Offline Mode**: Cache Master Prompt, generate without internet (simulation)
- [ ] **Multi-Language UI**: Extension interface in German, French, Spanish

---

## Publishing to Chrome Web Store

### Requirements
- Developer account ($5 one-time fee)
- Privacy policy URL
- Extension icons (16×16, 48×48, 128×128)
- Screenshots (1280×800 or 640×400)
- Promotional images (optional)

### Steps

1. **Prepare Package**
   ```bash
   cd chrome-extension
   zip -r marketplace-generator-v1.0.zip . -x "*.git*" "README.md"
   ```

2. **Create Developer Account**
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Pay $5 registration fee

3. **Upload Extension**
   - Click "New Item"
   - Upload ZIP file
   - Fill out store listing:
     - Title: "Marketplace Description Generator"
     - Short description: "AI-powered descriptions for eBay, Vinted, Kleinanzeigen"
     - Detailed description: (Use content from this README)
     - Category: Shopping
     - Language: English (add German, French as additional)
   - Upload screenshots
   - Submit for review

4. **Review Process**
   - Takes 1-3 business days
   - May require privacy policy for API key usage
   - May require explanation of host_permissions

---

## Privacy Policy

### Data Collection
This extension:
- ✅ Stores API key locally (not transmitted anywhere except Anthropic)
- ✅ Sends item data to Anthropic API for description generation
- ❌ Does NOT collect usage analytics
- ❌ Does NOT sell data to third parties
- ❌ Does NOT track browsing history

### Data Transmission
- **To Anthropic API**: Item title, condition, price, defects (for generation)
- **To Extension**: Generated descriptions, metadata
- **Encrypted**: All API calls use HTTPS

### Data Storage
- **API Key**: Stored in `chrome.storage.local` (browser-encrypted)
- **User Input**: Not stored, cleared on popup close
- **Generated Descriptions**: Not stored, only displayed in session

For full privacy policy template, see: [Chrome Web Store Privacy Policy Requirements](https://developer.chrome.com/docs/webstore/program-policies/)

---

## License

MIT License - Same as main Prompt Mutation Framework

---

## Support

### Report Issues
- GitHub Issues: [your-repo/issues](https://github.com/your-repo/prompt-mutation-framework/issues)
- Tag: `chrome-extension`

### Get Help
- Documentation: [Main README](../README.md)
- Demo: [Web Demo](../demo/README.md)
- Validation: [Test Results](../tests/VALIDATION_RESULTS.md)

---

## Changelog

**v1.0.0** (2025-11-17)
- ✅ Initial release
- ✅ Support for eBay, Vinted, Kleinanzeigen
- ✅ 3-variant generation (Emotional, Value, Trust)
- ✅ Auto-insert to marketplace forms
- ✅ Metadata display (risk score, modules, budget)
- ✅ Secure API key storage
- ✅ Beautiful gradient UI

---

**Status**: ✅ Production-Ready

**Supported Platforms**: 5 (eBay.de, eBay.com, Vinted.de, Vinted.fr, Kleinanzeigen)

**Framework Version**: 1.0 (Iteration 16 Master Prompt)

**Last Updated**: 2025-11-17
