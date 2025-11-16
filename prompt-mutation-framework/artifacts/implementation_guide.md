# Implementation Guide
## Deploying the Marketplace Prompt Framework in Production

This guide walks you through integrating the Prompt Mutation Framework into your marketplace automation application.

---

## TABLE OF CONTENTS

1. System Architecture
2. Quick Start (15-minute MVP)
3. Production Deployment
4. API Integration Points
5. Performance Optimization
6. Maintenance Schedule
7. Troubleshooting

---

## 1. SYSTEM ARCHITECTURE

### Recommended Stack

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│         (Web app, mobile app, browser extension)         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 APPLICATION LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Input      │  │   Prompt     │  │   Output     │  │
│  │ Validation   │→ │  Execution   │→ │  Formatting  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    AI LAYER                              │
│   ┌────────────────────────────────────────────┐        │
│   │  ITERATION 16 (Master Prompt)              │        │
│   │  - 7-Phase Execution                       │        │
│   │  - Category Routing                        │        │
│   │  - Specialist Modules (11-15)              │        │
│   └────────────────────────────────────────────┘        │
│                                                          │
│   LLM Provider: Claude, GPT-4, Gemini, etc.             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  DATA LAYER (Optional)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Price      │  │   Image      │  │   Serial     │  │
│  │  Database    │  │   Reverse    │  │  Number DB   │  │
│  │   API        │  │   Search     │  │    API       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack Recommendations

**Backend (Choose One)**:
- Python + FastAPI (recommended - easy LLM integration)
- Node.js + Express (good for JavaScript ecosystem)
- Ruby on Rails (if already using Rails)

**LLM Provider (Choose One)**:
- Anthropic Claude (best instruction following, safety-aware)
- OpenAI GPT-4 (strong performance, widely supported)
- Google Gemini (cost-effective, multilingual)
- Open-source (Llama 3, Mixtral - for self-hosting)

**Database**:
- PostgreSQL (structured data: user accounts, listings)
- Redis (caching: prompt outputs, market prices)

**Optional Enhancements**:
- Price API: eBay Sold Listings API, PriceCharting API
- Image Analysis: Google Cloud Vision, AWS Rekognition
- Translation: DeepL API (better than Google for EU languages)

---

## 2. QUICK START (15-Minute MVP)

### Step 1: Install Dependencies

```bash
# Python example
pip install anthropic openai python-dotenv

# Node.js example
npm install @anthropic-ai/sdk openai dotenv
```

### Step 2: Create Basic Integration

```python
# quickstart.py - Minimal viable implementation

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Load Master Prompt (Iteration 16)
with open("iterations/iteration_16_master_prompt.md", "r") as f:
    MASTER_PROMPT = f.read()

def generate_description(input_data):
    """
    Generate marketplace description from item data.

    Args:
        input_data (dict): Item information
            Required: item_category, brand_model, condition_raw, defects,
                     photos_type, price_asking, target_platform, target_language

    Returns:
        dict: Generated descriptions (variants A, B, C)
    """

    # Build user message with input data
    user_message = f"""
    Generate marketplace description for:

    {input_data}

    Use the Master Prompt framework (Iteration 16) to:
    1. Classify category and route to appropriate specialist
    2. Calculate risk score
    3. Determine character budget
    4. Generate 3 variants (emotion, value, trust-optimized)

    Return JSON format with variant_a_emotion, variant_b_value, variant_c_trust.
    """

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system=MASTER_PROMPT,  # Full framework as system prompt
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return message.content

# Example usage
if __name__ == "__main__":
    sample_item = {
        "item_category": "smartphones",
        "brand_model": "Apple iPhone 13 Pro 256GB Sierra Blue",
        "condition_raw": "excellent",
        "defects": ["small screen scratch"],
        "photos_type": "actual",
        "price_asking": 549,
        "market_price_reference": 1149,
        "battery_health": 87,
        "included_items": ["USB-C cable", "case"],
        "target_platform": "eBay.de",
        "target_language": "de"
    }

    result = generate_description(sample_item)
    print(result)
```

### Step 3: Test the MVP

```bash
python quickstart.py
```

Expected output: 3 description variants in German optimized for eBay.de

**MVP Limitations**:
- No input validation
- No caching (expensive API calls)
- No error handling
- Missing external data integration

Time to production-ready: 15 minutes (MVP) → 2-4 weeks (production)

---

## 3. PRODUCTION DEPLOYMENT

### 3.1 Input Validation Layer

```python
# validators.py

from typing import List, Optional
from pydantic import BaseModel, field_validator, Field

class MarketplaceItemInput(BaseModel):
    """Validated input schema"""

    # Required fields
    item_category: str = Field(..., min_length=2, max_length=50)
    brand_model: str = Field(..., min_length=2, max_length=200)
    condition_raw: str
    defects: List[str] = Field(default_factory=list)
    photos_type: str = Field(..., pattern="^(actual|stock|none)$")
    price_asking: float = Field(..., gt=0, lt=1000000)
    target_platform: str
    target_language: str = Field(..., pattern="^[a-z]{2}$")

    # Optional fields
    market_price_reference: Optional[float] = None
    included_items: List[str] = Field(default_factory=list)
    serial_number: Optional[str] = None
    battery_health: Optional[int] = Field(None, ge=0, le=100)
    measurements: Optional[dict] = None

    @field_validator('item_category')
    @classmethod
    def validate_category(cls, v):
        VALID_CATEGORIES = [
            "smartphones", "laptops", "tablets", "luxury_handbags",
            "luxury_watches", "mens_clothing", "womens_clothing",
            "shoes", "furniture", "home_decor"
            # ... add all 50 categories
        ]
        if v not in VALID_CATEGORIES:
            # Could auto-map to nearest category
            raise ValueError(f"Category '{v}' not recognized")
        return v

    @field_validator('defects')
    @classmethod
    def check_critical_defects(cls, v):
        CRITICAL_DEFECTS = [
            "battery swelling", "fire hazard", "electrical shock",
            "asbestos", "toxic materials"
        ]
        if any(defect in CRITICAL_DEFECTS for defect in v):
            raise ValueError(f"CRITICAL: Item cannot be listed due to safety hazard: {v}")
        return v

# Usage
try:
    validated_input = MarketplaceItemInput(**user_data)
except ValidationError as e:
    return {"error": str(e), "status": 400}
```

### 3.2 Prompt Execution with Error Handling

```python
# prompt_executor.py

import time
from anthropic import AnthropicError
from tenacity import retry, stop_after_attempt, wait_exponential

class PromptExecutor:
    def __init__(self, api_key, cache_client=None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cache = cache_client  # Redis connection
        self.master_prompt = self._load_prompt()

    def _load_prompt(self):
        """Load Master Prompt with specialist modules"""
        with open("iterations/iteration_16_master_prompt.md", "r") as f:
            return f.read()

    def _get_cache_key(self, input_data):
        """Generate cache key from input data"""
        import hashlib
        import json
        data_str = json.dumps(input_data, sort_keys=True)
        return f"desc_{hashlib.md5(data_str.encode()).hexdigest()}"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def execute(self, input_data: dict) -> dict:
        """
        Execute prompt with caching, retries, and error handling
        """

        # Check cache first
        if self.cache:
            cache_key = self._get_cache_key(input_data)
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return json.loads(cached_result)

        try:
            # Execute prompt
            start_time = time.time()

            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                temperature=0.3,  # Lower temp for consistent output
                system=self.master_prompt,
                messages=[{
                    "role": "user",
                    "content": self._build_user_message(input_data)
                }]
            )

            execution_time = time.time() - start_time

            # Parse response
            result = self._parse_response(message.content)

            # Add metadata
            result["metadata"]["execution_time_ms"] = int(execution_time * 1000)
            result["metadata"]["model_used"] = "claude-sonnet-4-5"
            result["metadata"]["cache_hit"] = False

            # Cache result (24 hours)
            if self.cache:
                self.cache.setex(
                    cache_key,
                    86400,  # 24 hours
                    json.dumps(result)
                )

            return result

        except AnthropicError as e:
            # Log error
            logging.error(f"Anthropic API error: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise

    def _build_user_message(self, input_data):
        """Convert input dict to structured prompt"""
        return f"""
Generate marketplace description with the following data:

REQUIRED INPUTS:
- Category: {input_data['item_category']}
- Brand/Model: {input_data['brand_model']}
- Condition: {input_data['condition_raw']}
- Defects: {', '.join(input_data['defects']) if input_data['defects'] else 'None'}
- Photos: {input_data['photos_type']}
- Price: €{input_data['price_asking']}
- Platform: {input_data['target_platform']}
- Language: {input_data['target_language']}

OPTIONAL INPUTS:
{self._format_optional_fields(input_data)}

Execute all 7 phases of the Master Prompt framework.
Return JSON with variants and metadata.
"""

    def _parse_response(self, content):
        """Parse LLM response into structured format"""
        import json
        import re

        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', content[0].text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # Fallback: structure the text response
            return {
                "variant_a_emotion": self._extract_variant(content, "A"),
                "variant_b_value": self._extract_variant(content, "B"),
                "variant_c_trust": self._extract_variant(content, "C"),
                "metadata": {"structured_output": False}
            }
```

### 3.3 Output Formatting & Delivery

```python
# output_formatter.py

class OutputFormatter:
    """Format prompt output for various platforms"""

    def format_for_ebay(self, result: dict) -> str:
        """Format for eBay listing (HTML supported)"""
        variant = result["variant_b_value"]  # Value-optimized for eBay

        return f"""
<div class="marketplace-listing">
    <h2>{variant['text'][:80]}</h2>
    <p>{variant['text']}</p>

    <div class="item-specifics">
        <strong>Condition:</strong> {self._condition_text(variant)}<br>
        <strong>Included:</strong> {self._included_items(variant)}
    </div>
</div>
"""

    def format_for_vinted(self, result: dict) -> str:
        """Format for Vinted (plain text, casual)"""
        variant = result["variant_a_emotion"]  # Emotion-optimized for Vinted
        return variant['text']  # Vinted uses plain text

    def format_for_api(self, result: dict) -> dict:
        """Format for API response (JSON)"""
        return {
            "status": "success",
            "descriptions": {
                "emotion_optimized": result["variant_a_emotion"],
                "value_optimized": result["variant_b_value"],
                "trust_optimized": result["variant_c_trust"]
            },
            "metadata": result["metadata"],
            "recommendations": result.get("recommendations", {})
        }
```

---

## 4. API INTEGRATION POINTS

### 4.1 Price Database Integration

```python
# integrations/price_api.py

import requests

class PriceDataProvider:
    """Integrate with eBay Sold Listings API or similar"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ebay.com/buy/browse/v1"

    def get_market_price(self, brand_model, category, condition):
        """
        Fetch recent sold prices for comparable items

        Returns:
            dict: {
                "average": float,
                "min": float,
                "max": float,
                "recent_sales": List[float],
                "data_freshness": datetime
            }
        """

        # Search for sold listings
        response = requests.get(
            f"{self.base_url}/item_summary/search",
            params={
                "q": f"{brand_model} {condition}",
                "category_ids": category,
                "filter": "buyingOptions:{FIXED_PRICE},itemEndDate:[2024-01-01T00:00:00.000Z..2024-12-31T23:59:59.999Z]",
                "sort": "price",
                "limit": 50
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

        data = response.json()
        prices = [item['price']['value'] for item in data.get('itemSummaries', [])]

        if prices:
            return {
                "average": sum(prices) / len(prices),
                "min": min(prices),
                "max": max(prices),
                "recent_sales": prices,
                "data_freshness": datetime.now()
            }
        else:
            return None

# Usage in prompt executor
price_provider = PriceDataProvider(api_key=os.environ.get("EBAY_API_KEY"))
market_data = price_provider.get_market_price(
    brand_model="iPhone 13 Pro",
    category="smartphones",
    condition="excellent"
)

if market_data:
    input_data["market_price_reference"] = market_data["average"]
    input_data["price_comparable_range"] = f"{market_data['min']}-{market_data['max']}"
```

### 4.2 Image Reverse Search (Counterfeit Detection)

```python
# integrations/image_search.py

from google.cloud import vision

class ImageAuthenticator:
    """Check if uploaded photos are stock images or actual item"""

    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def reverse_search(self, image_url: str) -> dict:
        """
        Check if image appears elsewhere on web (stock photo detection)

        Returns:
            dict: {
                "is_stock_photo": bool,
                "matches_found": int,
                "confidence": float
            }
        """

        image = vision.Image()
        image.source.image_uri = image_url

        response = self.client.web_detection(image=image)
        web_detection = response.web_detection

        exact_matches = len(web_detection.full_matching_images)
        partial_matches = len(web_detection.partial_matching_images)

        # If image appears on >3 websites, likely stock photo
        is_stock = (exact_matches + partial_matches) > 3

        return {
            "is_stock_photo": is_stock,
            "matches_found": exact_matches + partial_matches,
            "confidence": min(1.0, (exact_matches + partial_matches) / 10)
        }
```

---

## 5. PERFORMANCE OPTIMIZATION

### 5.1 Caching Strategy

```python
# caching.py

import redis
import hashlib
import json

class PromptCache:
    """Redis-based caching for prompt outputs"""

    def __init__(self, redis_url):
        self.redis_client = redis.from_url(redis_url)

    def get(self, input_data: dict) -> Optional[dict]:
        """Retrieve cached result"""
        cache_key = self._generate_key(input_data)
        cached = self.redis_client.get(cache_key)
        return json.loads(cached) if cached else None

    def set(self, input_data: dict, result: dict, ttl=86400):
        """Cache result for 24 hours (default)"""
        cache_key = self._generate_key(input_data)
        self.redis_client.setex(
            cache_key,
            ttl,
            json.dumps(result)
        )

    def _generate_key(self, input_data: dict) -> str:
        """Create deterministic cache key"""
        # Sort keys for consistency
        sorted_data = json.dumps(input_data, sort_keys=True)
        return f"prompt:v16:{hashlib.sha256(sorted_data.encode()).hexdigest()}"

# Cache hit rate should be 40-60% for typical marketplace usage
```

### 5.2 Batch Processing

```python
# batch_processor.py

import asyncio
from typing import List

class BatchProcessor:
    """Process multiple items in parallel"""

    def __init__(self, executor, max_concurrent=10):
        self.executor = executor
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_item(self, item_data):
        """Process single item with rate limiting"""
        async with self.semaphore:
            return await asyncio.to_thread(
                self.executor.execute,
                item_data
            )

    async def process_batch(self, items: List[dict]) -> List[dict]:
        """Process up to 100 items in parallel"""
        tasks = [self.process_item(item) for item in items]
        return await asyncio.gather(*tasks)

# Usage
async def main():
    batch_processor = BatchProcessor(prompt_executor, max_concurrent=10)
    results = await batch_processor.process_batch(items_list)

# Process 100 items in ~30 seconds vs. 5 minutes sequential
```

---

## 6. MAINTENANCE SCHEDULE

### Quarterly (Every 3 Months)
- [ ] Review platform rule changes (eBay, Vinted policy updates)
- [ ] Update fee structures in Iteration 8 platform profiles
- [ ] Check for new device models (smartphones, laptops) - update examples
- [ ] Review luxury brand authentication methods (counterfeiters evolve)
- [ ] Audit emotional hook libraries for trending language

### Biannually (Every 6 Months)
- [ ] Size conversion chart accuracy check (fashion sizing can shift)
- [ ] Language multiplier validation (test all 24 languages)
- [ ] Performance metrics review (cache hit rate, API costs)
- [ ] User feedback analysis (what prompts work best?)

### Annually
- [ ] Complete framework audit against Iteration 4 rubric
- [ ] Competitive analysis (new marketplace automation tools)
- [ ] Consider new specialist modules (categories 16-20?)
- [ ] LLM provider evaluation (is Claude still best, or switch to GPT-5/Gemini 2?)

### As Needed
- [ ] Platform launches (add new marketplace like Wallapop, Shpock)
- [ ] Category additions (user requests for vehicles, real estate)
- [ ] Critical safety updates (new recall categories, regulations)

---

## 7. TROUBLESHOOTING

### Issue: Descriptions Too Short/Long

**Symptom**: Output violates character budget
**Cause**: Language multiplier incorrect or budget calculation error
**Fix**:
```python
# Debug character budget calculation
print(f"Base budget: {base_budget}")
print(f"Language: {target_language}, Multiplier: {multipliers[target_language]}")
print(f"Adjustments: risk_score={risk_score}, platform={platform}")
print(f"Final budget: {final_budget}")
```

### Issue: Wrong Specialist Module Applied

**Symptom**: Luxury item gets tech specialist treatment
**Cause**: Category routing ambiguity
**Fix**:
```python
# Add logging to routing logic
logging.info(f"Category: {item_category}")
logging.info(f"Price: {price_asking}")
logging.info(f"Routing decision: {selected_module}")

# Add price-based override for luxury
if price_asking > 1000 and any(luxury_keyword in brand_model.lower() for luxury_keyword in ["hermès", "rolex", "louis vuitton"]):
    selected_module = "iteration_11_luxury"
```

### Issue: API Rate Limits

**Symptom**: "RateLimitError" from Anthropic/OpenAI
**Cause**: Exceeding requests per minute
**Fix**:
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=50, period=60)  # 50 calls per minute
def execute_prompt(input_data):
    return client.messages.create(...)
```

### Issue: Cache Stale Data

**Symptom**: Market prices outdated
**Cause**: Cache TTL too long
**Fix**:
```python
# Reduce cache TTL for price-sensitive data
cache.setex(key, ttl=3600)  # 1 hour instead of 24

# OR invalidate cache when price data updates
def update_market_prices():
    # Fetch new prices
    new_prices = price_api.get_latest()
    # Clear related cache entries
    cache.delete_pattern("prompt:*:price_*")
```

---

## COST ESTIMATION

### API Costs (Monthly, 1000 Listings)

**Anthropic Claude Sonnet 4.5**:
- Input: ~2000 tokens (Master Prompt + user input) × 1000 = 2M tokens × $0.003/1K = $6
- Output: ~300 tokens average × 1000 = 300K tokens × $0.015/1K = $4.50
- **Total: ~$10.50/month for 1000 listings** (with 50% cache hit rate: ~$5.25)

**OpenAI GPT-4**:
- Input: 2M tokens × $0.01/1K = $20
- Output: 300K tokens × $0.03/1K = $9
- **Total: ~$29/month for 1000 listings** (with cache: ~$14.50)

**Cost Optimization**:
- Use caching (50-60% hit rate typical)
- Batch requests where possible
- Consider cheaper models for simple categories (Haiku for fashion, Sonnet for luxury/tech)

### Infrastructure Costs (Monthly)

- Redis cache (AWS ElastiCache): $15-30/month
- Hosting (AWS EC2 t3.small): $15/month
- Price API (eBay): $50-200/month (optional)
- **Total infrastructure: $80-245/month**

**Break-even**: ~500 listings/month at €0.50/listing fee

---

## NEXT STEPS

1. **Week 1**: Implement quickstart MVP, test with 10 sample items
2. **Week 2**: Add input validation and error handling
3. **Week 3**: Integrate caching and batch processing
4. **Week 4**: Deploy to staging, user acceptance testing
5. **Week 5-6**: Production deployment with monitoring
6. **Week 7+**: Iterate based on user feedback and performance metrics

This framework is designed to scale from side project (100 listings/month) to enterprise (100,000+ listings/month) with proper caching and infrastructure.
