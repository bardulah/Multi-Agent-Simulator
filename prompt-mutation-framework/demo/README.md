# Demo Application - Marketplace Description Generator

A full-stack web application demonstrating the Prompt Mutation Framework in action.

## Features

- ✨ **3-Variant Generation**: Emotion, Value, and Trust-optimized descriptions
- 🎯 **Smart Routing**: Automatic specialist module selection
- 🛡️ **Safety Scoring**: Real-time fraud and hazard detection
- 🌍 **Multilingual**: Support for 24 EU languages
- 📊 **Metadata Display**: Risk scores, character budgets, modules applied
- 💻 **Live Demo**: Works without API key (simulation mode)

## Quick Start

### Option 1: Simulation Mode (No API Key Required)

```bash
# 1. Navigate to demo backend
cd demo/backend

# 2. Start the API server
python main.py

# 3. Open frontend in browser
# Open demo/frontend/index.html in your web browser
# Or serve with: python -m http.server 8001 (from demo/frontend directory)
```

### Option 2: Production Mode (With API Key)

```bash
# 1. Set API key
export ANTHROPIC_API_KEY=your_key_here

# 2. Start the API server
cd demo/backend
python main.py

# 3. Open frontend
open ../frontend/index.html
```

## Architecture

```
demo/
├── backend/           # FastAPI REST API
│   └── main.py       # API server with Master Prompt integration
│
└── frontend/         # Single-page web app
    └── index.html    # HTML/CSS/JavaScript interface
```

### Backend API Endpoints

**Base URL**: `http://localhost:8000`

#### `POST /api/generate`
Generate marketplace descriptions

**Request:**
```json
{
  "item_category": "smartphones",
  "brand_model": "Apple iPhone 13 Pro 256GB",
  "condition_raw": "excellent",
  "defects": ["small screen scratch"],
  "photos_type": "actual",
  "price_asking": 549,
  "target_platform": "eBay.de",
  "target_language": "de",
  "market_price_reference": 1149,
  "battery_health": 87
}
```

**Response:**
```json
{
  "variant_a_emotion": {
    "text": "Top-Gerät📸 Apple★★★★ €549 (52% off)",
    "char_count": 35,
    "optimization_focus": "Emotional appeal"
  },
  "variant_b_value": {
    "text": "Sparen Sie! Apple📸★★★★ €549 (52% off)",
    "char_count": 38,
    "optimization_focus": "Price value"
  },
  "variant_c_trust": {
    "text": "Geprüft📸 Apple★★★★ €549 (52% off)",
    "char_count": 33,
    "optimization_focus": "Trust signals"
  },
  "metadata": {
    "risk_score": 0,
    "risk_level": "LOW",
    "modules_applied": [
      "iteration_12_tech_specialist",
      "iteration_15_price_optimization"
    ],
    "character_budget": 160,
    "safety_warnings": []
  },
  "generated_at": "2025-11-17T08:15:30.123456",
  "simulation_mode": true
}
```

#### `GET /api/categories`
List supported product categories

#### `GET /api/platforms`
List supported marketplace platforms

#### `GET /health`
Health check endpoint

#### `GET /docs`
Interactive API documentation (Swagger UI)

## Deployment

### Deploy to Railway.app (Recommended)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd demo/backend
railway init

# 4. Add environment variable
railway variables set ANTHROPIC_API_KEY=your_key

# 5. Deploy
railway up

# 6. Open deployment
railway open
```

### Deploy to Render.com

1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `ANTHROPIC_API_KEY`

### Deploy to Vercel (Frontend)

```bash
# From demo/frontend directory
vercel --prod
```

Update `API_URL` in `index.html` to your deployed backend URL.

## Usage Examples

### Example 1: iPhone

```javascript
{
  "item_category": "smartphones",
  "brand_model": "Apple iPhone 13 Pro 256GB Sierra Blue",
  "condition_raw": "excellent",
  "defects": ["small screen scratch"],
  "photos_type": "actual",
  "price_asking": 549,
  "target_platform": "eBay.de",
  "target_language": "de",
  "market_price_reference": 1149,
  "battery_health": 87,
  "included_items": ["USB-C cable", "case"]
}
```

**Generated (Value Variant):**
```
Sparen Sie! Apple📸★★★★ €549 (52% off)
```

### Example 2: Hermès Birkin (High-Value Luxury)

```javascript
{
  "item_category": "luxury_handbags",
  "brand_model": "Hermès Birkin 30 Togo Leather",
  "condition_raw": "excellent",
  "defects": [],
  "photos_type": "actual",
  "price_asking": 12000,
  "target_platform": "eBay.de",
  "target_language": "en",
  "market_price_reference": 16000
}
```

**Result:**
- ✅ Routes to: `iteration_11_luxury_specialist`
- ✅ Risk: LOW (0/100)
- ✅ Budget: 165 chars (luxury expansion applied)

### Example 3: Potential Counterfeit (HIGH RISK)

```javascript
{
  "item_category": "luxury_handbags",
  "brand_model": "Louis Vuitton Neverfull MM",
  "condition_raw": "excellent",
  "defects": [],
  "photos_type": "stock",  // RED FLAG
  "price_asking": 400,
  "target_platform": "Vinted",
  "target_language": "en",
  "market_price_reference": 1200  // 67% below market
}
```

**Result:**
- ⚠️ Risk: HIGH (65/100)
- ⚠️ Warning: "Stock photos only - authentication recommended"
- ✅ Budget expanded to 180 chars (max) for safety warnings

## Testing the Demo

### Manual Testing

1. **Open Frontend**: http://localhost:8001 (or open index.html directly)
2. **Click "Load Example"** - Fills form with iPhone test data
3. **Click "Generate Descriptions"** - Calls API
4. **Review Results**:
   - 3 variants displayed
   - Metadata showing risk score, modules, budget
   - Copy buttons for each variant

### Automated Testing

```bash
# Test API health
curl http://localhost:8000/health

# Test generation endpoint
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

**test_data.json:**
```json
{
  "item_category": "smartphones",
  "brand_model": "Apple iPhone 13 Pro 256GB",
  "condition_raw": "excellent",
  "defects": [],
  "photos_type": "actual",
  "price_asking": 549,
  "target_platform": "eBay.de",
  "target_language": "de"
}
```

## Performance

### Simulation Mode (No API)
- Response time: <50ms
- Cost: $0 (free)
- Use for: Demo, testing, development

### Production Mode (Claude API)
- Response time: 1.5-3 seconds
- Cost: ~$0.01 per generation
- Tokens: ~2000 input + 300 output
- Use for: Real marketplace automation

### Caching (Future Enhancement)
- Add Redis caching layer
- Cache hit rate: 40-60% expected
- Cost reduction: 50%

## Security

### CORS Configuration

Production settings in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### API Key Protection

Never expose `ANTHROPIC_API_KEY` in frontend or commit to Git.

**Good:**
```bash
# Backend .env file (gitignored)
ANTHROPIC_API_KEY=sk-ant-xxx
```

**Bad:**
```javascript
// ❌ NEVER do this in frontend
const API_KEY = "sk-ant-xxx";  // Exposed to users!
```

## Troubleshooting

### Issue: CORS Error

**Symptom:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Fix:**
Ensure CORS middleware is configured in `main.py` (already set to `allow_origins=["*"]` for development)

### Issue: API Not Found

**Symptom:**
```
Failed to fetch: TypeError: Failed to fetch
```

**Fix:**
1. Check API is running: `http://localhost:8000/health`
2. Update `API_URL` in index.html if using different port

### Issue: Empty Results

**Symptom:**
Results display but variants are empty

**Fix:**
- Check browser console for errors
- Verify API response structure matches expected format
- Try with example data first ("Load Example" button)

## Customization

### Change Styling

Edit CSS in `frontend/index.html` `<style>` section:
```css
/* Change primary color */
button {
    background: linear-gradient(135deg, #YOUR_COLOR 0%, #YOUR_COLOR 100%);
}
```

### Add New Category

1. Update `backend/main.py`:
```python
@app.get("/api/categories")
async def get_categories():
    return {
        "categories": [
            # ... existing categories
            {"id": "bicycles", "name": "Bicycles", "specialist": "Base Framework"},
        ]
    }
```

2. Update `frontend/index.html`:
```html
<select id="category">
    <!-- ... existing options -->
    <option value="bicycles">Bicycles</option>
</select>
```

### Add New Language

Update both backend routing and frontend hooks dictionary:
```javascript
const hooks = {
    // ... existing languages
    "nl": {"emotion": "Geweldig", "value": "Bespaar", "trust": "Geverifieerd"}
};
```

## Next Steps

1. **Add Authentication**: JWT tokens for API access control
2. **Add Database**: Store generated descriptions for analytics
3. **Add Analytics**: Track which variants convert best
4. **Add Image Upload**: Analyze photos to detect stock vs. actual
5. **Add Bulk Processing**: CSV upload for batch generation

## License

MIT License - See main project README

---

**Demo Status**: ✅ Fully Functional

**Last Updated**: 2025-11-17

**Framework Version**: v1.0 (Iteration 16 Master Prompt)
