/**
 * Background Service Worker
 * Handles API calls to generate descriptions
 */

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GENERATE_DESCRIPTION') {
        handleGeneration(message.data)
            .then(result => sendResponse({ success: true, result }))
            .catch(error => sendResponse({ success: false, error: error.message }));

        // Return true to indicate async response
        return true;
    }
});

/**
 * Generate marketplace description using Framework
 */
async function handleGeneration(data) {
    const { apiKey, itemTitle, condition, price, defects, platform } = data;

    // Determine category from title (simple heuristic)
    const category = detectCategory(itemTitle);

    // Determine language from platform
    const language = platform.includes('.de') ? 'de' :
                    platform.includes('.fr') ? 'fr' :
                    platform.includes('.es') ? 'es' : 'en';

    // Build prompt for Master Prompt
    const userPrompt = buildUserPrompt({
        category,
        itemTitle,
        condition,
        price,
        defects,
        platform,
        language
    });

    // Call Anthropic API
    const result = await callAnthropicAPI(apiKey, userPrompt);

    return result;
}

/**
 * Detect item category from title
 */
function detectCategory(title) {
    const titleLower = title.toLowerCase();

    // Tech
    if (titleLower.match(/iphone|samsung|pixel|galaxy|smartphone|phone/)) {
        return 'smartphones';
    }
    if (titleLower.match(/macbook|laptop|notebook|thinkpad|dell|hp/)) {
        return 'laptops';
    }
    if (titleLower.match(/ipad|tablet|kindle/)) {
        return 'tablets';
    }
    if (titleLower.match(/playstation|ps5|ps4|xbox|nintendo|switch/)) {
        return 'gaming_consoles';
    }

    // Luxury
    if (titleLower.match(/hermes|hermès|birkin|kelly|chanel|louis vuitton|gucci|prada/)) {
        return 'luxury_handbags';
    }
    if (titleLower.match(/rolex|omega|patek|cartier|watch/)) {
        return 'luxury_watches';
    }

    // Clothing
    if (titleLower.match(/dress|shirt|pants|jeans|jacket|coat/)) {
        return 'clothing';
    }
    if (titleLower.match(/shoes|sneakers|boots|heels|nike|adidas/)) {
        return 'shoes';
    }

    // Furniture
    if (titleLower.match(/sofa|couch|table|chair|desk|shelf|bed|ikea/)) {
        return 'furniture';
    }

    // Default
    return 'general';
}

/**
 * Build user prompt for Master Prompt
 */
function buildUserPrompt(data) {
    const { category, itemTitle, condition, price, defects, platform, language } = data;

    return `
Generate marketplace description with the following data:

REQUIRED INPUTS:
- Category: ${category}
- Brand/Model: ${itemTitle}
- Condition: ${condition}
- Defects: ${defects.length > 0 ? defects.join(', ') : 'None'}
- Photos: actual
- Price: €${price}
- Platform: ${platform}
- Language: ${language}

Execute all 7 phases of the Master Prompt framework.
Return JSON with variant_a_emotion, variant_b_value, variant_c_trust, and metadata.

Response format:
{
  "variant_a_emotion": {"text": "...", "char_count": X, "optimization_focus": "..."},
  "variant_b_value": {"text": "...", "char_count": X, "optimization_focus": "..."},
  "variant_c_trust": {"text": "...", "char_count": X, "optimization_focus": "..."},
  "metadata": {
    "risk_score": X,
    "risk_level": "LOW/MEDIUM/HIGH/CRITICAL",
    "modules_applied": ["..."],
    "character_budget": X,
    "safety_warnings": ["..."]
  }
}
`.trim();
}

/**
 * Call Anthropic API
 */
async function callAnthropicAPI(apiKey, userPrompt) {
    // Load Master Prompt (embedded or fetched)
    const masterPrompt = getMasterPrompt();

    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
            model: 'claude-sonnet-4-5-20250929',
            max_tokens: 2048,
            temperature: 0.3,
            system: masterPrompt,
            messages: [
                {
                    role: 'user',
                    content: userPrompt
                }
            ]
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error?.message || 'API request failed');
    }

    const data = await response.json();
    const responseText = data.content[0].text;

    // Parse JSON from response
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
        throw new Error('Invalid response format from API');
    }

    const result = JSON.parse(jsonMatch[0]);

    return result;
}

/**
 * Get Master Prompt (embedded snippet)
 * In production, this should be the full Master Prompt from iteration_16_master_prompt.md
 */
function getMasterPrompt() {
    return `
# MASTER PROMPT: EU Marketplace Description Generator (v16 - Production)

You are an expert marketplace description generator for European secondhand platforms.

## PHASE 1: INPUT ANALYSIS
Analyze provided item data: category, condition, price, defects, photos, platform, language.

## PHASE 2: ROUTING & CONFIGURATION
Route to specialist modules based on category:
- Smartphones/Laptops → Tech Specialist (Iteration 12)
- Luxury items → Luxury Specialist (Iteration 11)
- Clothing → Clothing Specialist (Iteration 13)
- Furniture → Furniture Specialist (Iteration 14)

## PHASE 3: SAFETY & RISK SCORING
Calculate risk score (0-100):
- Luxury + low price + stock photos = HIGH RISK (counterfeit)
- Battery defects = CRITICAL RISK
- Other defects = LOW/MEDIUM RISK

## PHASE 4: CHARACTER BUDGET CALCULATION
Base: 100 chars
Adjustments:
- Language: German 1.25×, French 1.15×, Spanish 1.12×
- Platform: eBay +20, Vinted -10
- High price (>€500): +15
- High risk: +50
Range: 90-180 chars

## PHASE 5: MULTI-VARIANT GENERATION
Generate 3 variants:
- Variant A (Emotion): Emotionally appealing hook
- Variant B (Value): Price/discount focus
- Variant C (Trust): Verification/authenticity signals

Structure:
[Hook][Brand][Photo_Indicator][Condition_Stars][Price]

Example (German):
"Sparen Sie! Apple📸★★★★ €549 (52% off)"

## PHASE 6: COMPLIANCE VALIDATION
✓ Defects disclosed
✓ No misleading claims
✓ Accurate condition representation

## PHASE 7: OUTPUT
Return JSON with all 3 variants and metadata.

Execute all phases now.
`.trim();
}

// Log service worker activation
console.log('Marketplace Description Generator - Background Service Worker Activated');
