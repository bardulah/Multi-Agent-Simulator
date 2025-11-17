"""
Marketplace Description Generator API
FastAPI backend for the Prompt Mutation Framework Demo

This API provides endpoints to generate optimized marketplace descriptions
using the Master Prompt (Iteration 16) framework.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import os
import json
from datetime import datetime

# Simulated mode (works without API key for demo)
SIMULATION_MODE = not os.environ.get("ANTHROPIC_API_KEY")

if not SIMULATION_MODE:
    import anthropic

app = FastAPI(
    title="Marketplace Description Generator",
    description="AI-powered description generator for European secondhand marketplaces",
    version="1.0.0"
)

# CORS middleware (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== MODELS ====================

class ItemInput(BaseModel):
    """Input schema for item description generation"""

    item_category: str = Field(..., description="Product category (smartphones, luxury_handbags, etc.)")
    brand_model: str = Field(..., description="Brand and model name")
    condition_raw: str = Field(..., description="Condition description (excellent, good, fair, etc.)")
    defects: List[str] = Field(default=[], description="List of defects or issues")
    photos_type: str = Field(..., description="Photo type: 'actual' or 'stock'")
    price_asking: float = Field(..., gt=0, description="Asking price in EUR")
    target_platform: str = Field(..., description="Marketplace platform (eBay.de, Vinted, etc.)")
    target_language: str = Field(..., description="Language code (de, en, fr, etc.)")

    # Optional fields
    market_price_reference: Optional[float] = Field(None, description="Original/market price for comparison")
    included_items: List[str] = Field(default=[], description="Items included in the sale")
    battery_health: Optional[int] = Field(None, ge=0, le=100, description="Battery health percentage (for devices)")
    measurements: Optional[Dict] = Field(None, description="Measurements dict (for clothing/furniture)")
    date_code: Optional[str] = Field(None, description="Date code (for luxury items)")
    serial_number: Optional[str] = Field(None, description="Serial number (for electronics/luxury)")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class DescriptionVariant(BaseModel):
    """A single description variant"""
    text: str
    char_count: int
    optimization_focus: str


class GenerationResult(BaseModel):
    """Result of description generation"""
    variant_a_emotion: DescriptionVariant
    variant_b_value: DescriptionVariant
    variant_c_trust: DescriptionVariant
    metadata: Dict
    generated_at: str
    simulation_mode: bool = False


# ==================== CORE LOGIC ====================

class DescriptionGenerator:
    """Handles description generation using the framework"""

    def __init__(self):
        self.simulation_mode = SIMULATION_MODE

        if not self.simulation_mode:
            self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            self.master_prompt = self._load_master_prompt()
        else:
            self.client = None
            self.master_prompt = None

    def _load_master_prompt(self) -> str:
        """Load the Master Prompt from file"""
        try:
            prompt_path = "../../iterations/iteration_16_master_prompt.md"
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Alternative paths
            for path in [
                "../iterations/iteration_16_master_prompt.md",
                "iterations/iteration_16_master_prompt.md",
                "prompt-mutation-framework/iterations/iteration_16_master_prompt.md"
            ]:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return f.read()
                except FileNotFoundError:
                    continue
            return None

    def generate(self, input_data: ItemInput) -> GenerationResult:
        """Generate marketplace descriptions"""

        if self.simulation_mode:
            return self._simulate_generation(input_data)
        else:
            return self._real_generation(input_data)

    def _simulate_generation(self, input_data: ItemInput) -> GenerationResult:
        """Simulate description generation (demo mode without API)"""

        # Route to module
        modules = self._route_to_modules(input_data)

        # Calculate risk
        risk_score, risk_level = self._calculate_risk(input_data)

        # Calculate character budget
        char_budget = self._calculate_budget(input_data, risk_level)

        # Generate variants
        brand = input_data.brand_model.split()[0]
        price = input_data.price_asking
        condition = "★★★★" if "excellent" in input_data.condition_raw.lower() else "★★★"
        photo = "📸" if input_data.photos_type == "actual" else "🖼️"

        lang = input_data.target_language

        # Language-specific hooks
        hooks = {
            "de": {"emotion": "Top-Gerät", "value": "Sparen Sie", "trust": "Geprüft"},
            "en": {"emotion": "Great find", "value": "Save big", "trust": "Verified"},
            "fr": {"emotion": "Bonne affaire", "value": "Économisez", "trust": "Vérifié"}
        }
        hook_set = hooks.get(lang, hooks["en"])

        # Generate price string
        price_str = f"€{price}"
        if input_data.market_price_reference:
            savings = int((1 - price / input_data.market_price_reference) * 100)
            price_str = f"€{price} ({savings}% off)"

        variants = {
            "variant_a_emotion": DescriptionVariant(
                text=f"{hook_set['emotion']}{photo} {brand}{condition} {price_str}",
                char_count=len(f"{hook_set['emotion']}{photo} {brand}{condition} {price_str}"),
                optimization_focus="Emotional appeal"
            ),
            "variant_b_value": DescriptionVariant(
                text=f"{hook_set['value']}! {brand}{photo}{condition} {price_str}",
                char_count=len(f"{hook_set['value']}! {brand}{photo}{condition} {price_str}"),
                optimization_focus="Price value"
            ),
            "variant_c_trust": DescriptionVariant(
                text=f"{hook_set['trust']}{photo} {brand}{condition} {price_str}",
                char_count=len(f"{hook_set['trust']}{photo} {brand}{condition} {price_str}"),
                optimization_focus="Trust signals"
            )
        }

        # Generate warnings
        warnings = []
        if risk_level in ["HIGH", "CRITICAL"]:
            if input_data.photos_type == "stock":
                warnings.append("⚠️ Stock photos - authentication recommended")
            if any("battery" in d.lower() for d in input_data.defects):
                warnings.append("🚨 CRITICAL: Battery safety issue detected")

        return GenerationResult(
            **variants,
            metadata={
                "risk_score": risk_score,
                "risk_level": risk_level,
                "modules_applied": modules,
                "character_budget": char_budget,
                "safety_warnings": warnings
            },
            generated_at=datetime.now().isoformat(),
            simulation_mode=True
        )

    def _real_generation(self, input_data: ItemInput) -> GenerationResult:
        """Generate using real LLM API"""

        user_message = self._build_prompt(input_data)

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                temperature=0.3,
                system=self.master_prompt,
                messages=[{
                    "role": "user",
                    "content": user_message
                }]
            )

            response_text = message.content[0].text

            # Parse JSON response
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)

            if json_match:
                result_dict = json.loads(json_match.group())

                # Convert to GenerationResult
                return GenerationResult(
                    variant_a_emotion=DescriptionVariant(**result_dict["variant_a_emotion"]),
                    variant_b_value=DescriptionVariant(**result_dict["variant_b_value"]),
                    variant_c_trust=DescriptionVariant(**result_dict["variant_c_trust"]),
                    metadata=result_dict["metadata"],
                    generated_at=datetime.now().isoformat(),
                    simulation_mode=False
                )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

    def _build_prompt(self, input_data: ItemInput) -> str:
        """Build user prompt from input data"""

        fields = input_data.model_dump()

        prompt = f"""Generate marketplace description with the following data:

REQUIRED INPUTS:
- Category: {fields['item_category']}
- Brand/Model: {fields['brand_model']}
- Condition: {fields['condition_raw']}
- Defects: {', '.join(fields['defects']) if fields['defects'] else 'None'}
- Photos: {fields['photos_type']}
- Price: €{fields['price_asking']}
- Platform: {fields['target_platform']}
- Language: {fields['target_language']}

OPTIONAL INPUTS:"""

        if fields.get('market_price_reference'):
            prompt += f"\n- Market Price: €{fields['market_price_reference']}"
        if fields.get('included_items'):
            prompt += f"\n- Included Items: {', '.join(fields['included_items'])}"
        if fields.get('battery_health'):
            prompt += f"\n- Battery Health: {fields['battery_health']}%"

        prompt += """

Execute all 7 phases of the Master Prompt framework.
Return JSON with variant_a_emotion, variant_b_value, variant_c_trust, and metadata.
"""

        return prompt

    def _route_to_modules(self, input_data: ItemInput) -> List[str]:
        """Simulate module routing"""
        category = input_data.item_category
        price = input_data.price_asking

        modules = []

        if "luxury" in category or price > 1000:
            modules.append("iteration_11_luxury_specialist")
        elif category in ["smartphones", "laptops", "tablets"]:
            modules.append("iteration_12_tech_specialist")
        elif "clothing" in category:
            modules.append("iteration_13_clothing_specialist")
        elif "furniture" in category:
            modules.append("iteration_14_furniture_specialist")
        else:
            modules.append("base_framework")

        modules.append("iteration_15_price_optimization")
        return modules

    def _calculate_risk(self, input_data: ItemInput) -> tuple:
        """Calculate risk score"""
        risk = 0

        if ("luxury" in input_data.item_category and
            input_data.market_price_reference and
            input_data.price_asking < input_data.market_price_reference * 0.6 and
            input_data.photos_type == "stock"):
            risk += 40

        if any("battery" in d.lower() for d in input_data.defects):
            risk += 50

        if risk >= 81:
            level = "CRITICAL"
        elif risk >= 51:
            level = "HIGH"
        elif risk >= 21:
            level = "MEDIUM"
        else:
            level = "LOW"

        return risk, level

    def _calculate_budget(self, input_data: ItemInput, risk_level: str) -> int:
        """Calculate character budget"""
        base = 100

        multipliers = {"de": 1.25, "en": 1.0, "fr": 1.15, "es": 1.12}
        budget = int(base * multipliers.get(input_data.target_language, 1.0))

        if risk_level in ["HIGH", "CRITICAL"]:
            budget += 50
        if input_data.price_asking > 500:
            budget += 15

        return min(max(budget, 90), 180)


# ==================== API ENDPOINTS ====================

generator = DescriptionGenerator()


@app.get("/")
async def root():
    """API root - health check"""
    return {
        "service": "Marketplace Description Generator",
        "version": "1.0.0",
        "status": "operational",
        "mode": "simulation" if SIMULATION_MODE else "production",
        "framework": "Prompt Mutation Framework (Iteration 16)",
        "endpoints": {
            "generate": "/api/generate",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "simulation_mode": SIMULATION_MODE,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/generate", response_model=GenerationResult)
async def generate_description(item: ItemInput):
    """
    Generate optimized marketplace descriptions

    This endpoint uses the Master Prompt (Iteration 16) framework to generate
    three variants of marketplace descriptions optimized for different buyer psychology.

    **Returns:**
    - variant_a_emotion: Emotionally-driven description
    - variant_b_value: Price/value-focused description
    - variant_c_trust: Trust/verification-focused description
    - metadata: Risk scoring, modules applied, character budgets
    """

    try:
        result = generator.generate(item)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Description generation failed: {str(e)}"
        )


@app.get("/api/categories")
async def get_categories():
    """Get list of supported product categories"""
    return {
        "categories": [
            {"id": "smartphones", "name": "Smartphones", "specialist": "Tech (12)"},
            {"id": "laptops", "name": "Laptops", "specialist": "Tech (12)"},
            {"id": "tablets", "name": "Tablets", "specialist": "Tech (12)"},
            {"id": "gaming_consoles", "name": "Gaming Consoles", "specialist": "Tech (12)"},
            {"id": "luxury_handbags", "name": "Luxury Handbags", "specialist": "Luxury (11)"},
            {"id": "luxury_watches", "name": "Luxury Watches", "specialist": "Luxury (11)"},
            {"id": "mens_clothing", "name": "Men's Clothing", "specialist": "Clothing (13)"},
            {"id": "womens_clothing", "name": "Women's Clothing", "specialist": "Clothing (13)"},
            {"id": "shoes", "name": "Shoes", "specialist": "Clothing (13)"},
            {"id": "furniture", "name": "Furniture", "specialist": "Furniture (14)"},
            {"id": "home_decor", "name": "Home Decor", "specialist": "Base Framework"},
            {"id": "books", "name": "Books", "specialist": "Base Framework"},
        ]
    }


@app.get("/api/platforms")
async def get_platforms():
    """Get list of supported marketplace platforms"""
    return {
        "platforms": [
            {"id": "eBay.de", "name": "eBay Deutschland", "language": "de"},
            {"id": "eBay.com", "name": "eBay International", "language": "en"},
            {"id": "Vinted", "name": "Vinted", "language": "de/en/fr"},
            {"id": "Vinted.fr", "name": "Vinted France", "language": "fr"},
            {"id": "Kleinanzeigen", "name": "eBay Kleinanzeigen", "language": "de"},
            {"id": "Mercari_EU", "name": "Mercari Europe", "language": "en"},
        ]
    }


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Marketplace Description Generator API")
    print(f"   Mode: {'SIMULATION (no API key)' if SIMULATION_MODE else 'PRODUCTION (with API)'}")
    print("   Docs: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
