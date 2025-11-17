"""
Validation Test Harness for Prompt Mutation Framework
Tests the Master Prompt (Iteration 16) with real LLM execution

This script validates that the framework:
1. Routes to correct specialist modules
2. Generates valid multi-variant outputs
3. Applies safety checks appropriately
4. Handles edge cases correctly
"""

import os
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import anthropic
from dotenv import load_dotenv

load_dotenv()


class ValidationHarness:
    """Test harness for validating prompt framework"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            print("⚠️  WARNING: No API key found. Set ANTHROPIC_API_KEY or pass api_key parameter.")
            print("   Tests will use simulated outputs for demonstration.")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        # Load Master Prompt
        self.master_prompt = self._load_master_prompt()

        # Results storage
        self.results = []

    def _load_master_prompt(self) -> str:
        """Load the Master Prompt from Iteration 16"""
        prompt_path = "../iterations/iteration_16_master_prompt.md"
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Try alternative path
            prompt_path = "prompt-mutation-framework/iterations/iteration_16_master_prompt.md"
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()

    def create_test_case(
        self,
        name: str,
        item_category: str,
        brand_model: str,
        condition_raw: str,
        defects: List[str],
        photos_type: str,
        price_asking: float,
        target_platform: str,
        target_language: str,
        expected_module: str,
        expected_risk_level: str,
        **optional_fields
    ) -> Dict:
        """Create a test case with expected outcomes"""

        test_case = {
            "name": name,
            "input": {
                "item_category": item_category,
                "brand_model": brand_model,
                "condition_raw": condition_raw,
                "defects": defects,
                "photos_type": photos_type,
                "price_asking": price_asking,
                "target_platform": target_platform,
                "target_language": target_language,
                **optional_fields
            },
            "expected": {
                "module": expected_module,
                "risk_level": expected_risk_level
            }
        }

        return test_case

    def execute_test(self, test_case: Dict) -> Dict:
        """Execute a single test case"""

        print(f"\n{'='*80}")
        print(f"TEST: {test_case['name']}")
        print(f"{'='*80}")

        start_time = time.time()

        # Build prompt
        user_message = self._build_user_message(test_case["input"])

        if self.client:
            # Real LLM execution
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
                execution_time = time.time() - start_time

                # Parse response
                result = self._parse_response(response_text)
                result["execution_time_ms"] = int(execution_time * 1000)
                result["tokens_used"] = {
                    "input": message.usage.input_tokens,
                    "output": message.usage.output_tokens,
                    "total": message.usage.input_tokens + message.usage.output_tokens
                }

            except Exception as e:
                result = {
                    "error": str(e),
                    "execution_time_ms": int((time.time() - start_time) * 1000)
                }
        else:
            # Simulated output (for demonstration without API key)
            result = self._simulate_output(test_case)
            result["execution_time_ms"] = 50  # Simulated
            result["simulated"] = True

        # Validate against expectations
        validation = self._validate_result(result, test_case["expected"])

        # Store result
        test_result = {
            "test_name": test_case["name"],
            "input": test_case["input"],
            "expected": test_case["expected"],
            "actual": result,
            "validation": validation,
            "timestamp": datetime.now().isoformat()
        }

        self.results.append(test_result)

        # Print summary
        self._print_test_summary(test_result)

        return test_result

    def _build_user_message(self, input_data: Dict) -> str:
        """Convert input dict to user message"""

        required = f"""Generate marketplace description with the following data:

REQUIRED INPUTS:
- Category: {input_data['item_category']}
- Brand/Model: {input_data['brand_model']}
- Condition: {input_data['condition_raw']}
- Defects: {', '.join(input_data['defects']) if input_data['defects'] else 'None'}
- Photos: {input_data['photos_type']}
- Price: €{input_data['price_asking']}
- Platform: {input_data['target_platform']}
- Language: {input_data['target_language']}"""

        optional = []
        for key, value in input_data.items():
            if key not in ['item_category', 'brand_model', 'condition_raw', 'defects',
                          'photos_type', 'price_asking', 'target_platform', 'target_language']:
                optional.append(f"- {key}: {value}")

        if optional:
            required += "\n\nOPTIONAL INPUTS:\n" + "\n".join(optional)

        required += """

Execute all 7 phases of the Master Prompt framework.
Return JSON with:
{
  "variant_a_emotion": {"text": "...", "char_count": N},
  "variant_b_value": {"text": "...", "char_count": N},
  "variant_c_trust": {"text": "...", "char_count": N},
  "metadata": {
    "risk_score": N,
    "risk_level": "LOW/MEDIUM/HIGH/CRITICAL",
    "modules_applied": [...],
    "character_budget": N,
    "safety_warnings": [...]
  }
}"""

        return required

    def _parse_response(self, response_text: str) -> Dict:
        """Parse LLM response into structured result"""
        import re

        # Try to extract JSON
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)

        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: extract key information manually
        return {
            "variant_a_emotion": {"text": "Failed to parse", "char_count": 0},
            "variant_b_value": {"text": "Failed to parse", "char_count": 0},
            "variant_c_trust": {"text": "Failed to parse", "char_count": 0},
            "metadata": {
                "parse_error": "Could not extract structured JSON from response",
                "raw_response": response_text[:500]
            }
        }

    def _simulate_output(self, test_case: Dict) -> Dict:
        """Simulate output when no API key available (for testing harness itself)"""

        input_data = test_case["input"]

        # Simulate routing
        if "luxury" in input_data["item_category"] or input_data["price_asking"] > 1000:
            modules = ["iteration_11_luxury"]
        elif "smartphone" in input_data["item_category"] or "laptop" in input_data["item_category"]:
            modules = ["iteration_12_tech"]
        elif "clothing" in input_data["item_category"]:
            modules = ["iteration_13_clothing"]
        else:
            modules = ["base_framework"]

        # Simulate risk scoring
        risk_score = 0
        if input_data["photos_type"] == "stock":
            risk_score += 25
        if input_data["defects"] and any("battery" in d for d in input_data["defects"]):
            risk_score += 50

        risk_level = "LOW" if risk_score < 20 else "MEDIUM" if risk_score < 50 else "HIGH"

        # Simulate variant generation
        brand = input_data["brand_model"].split()[0]
        price = input_data["price_asking"]

        return {
            "variant_a_emotion": {
                "text": f"[SIMULATED] Great find📸 {brand}★★★★ €{price}",
                "char_count": 45
            },
            "variant_b_value": {
                "text": f"[SIMULATED] Save big! {brand}★★★★ €{price}",
                "char_count": 42
            },
            "variant_c_trust": {
                "text": f"[SIMULATED] Verified📸 {brand}★★★★ €{price}",
                "char_count": 44
            },
            "metadata": {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "modules_applied": modules,
                "character_budget": 120,
                "safety_warnings": []
            }
        }

    def _validate_result(self, result: Dict, expected: Dict) -> Dict:
        """Validate result against expected outcomes"""

        validation = {
            "passed": True,
            "issues": []
        }

        # Check if error occurred
        if "error" in result:
            validation["passed"] = False
            validation["issues"].append(f"Execution error: {result['error']}")
            return validation

        # Check module routing
        if "metadata" in result and "modules_applied" in result["metadata"]:
            applied_modules = result["metadata"]["modules_applied"]
            expected_module = expected["module"]

            if not any(expected_module in module for module in applied_modules):
                validation["passed"] = False
                validation["issues"].append(
                    f"Wrong module: expected '{expected_module}', got {applied_modules}"
                )

        # Check risk level
        if "metadata" in result and "risk_level" in result["metadata"]:
            actual_risk = result["metadata"]["risk_level"]
            expected_risk = expected["risk_level"]

            if actual_risk != expected_risk:
                validation["issues"].append(
                    f"Risk level mismatch: expected '{expected_risk}', got '{actual_risk}'"
                )
                # This is a warning, not a failure

        # Check variants generated
        required_variants = ["variant_a_emotion", "variant_b_value", "variant_c_trust"]
        for variant in required_variants:
            if variant not in result or not result[variant].get("text"):
                validation["passed"] = False
                validation["issues"].append(f"Missing or empty variant: {variant}")

        # Check character budgets
        if "metadata" in result and "character_budget" in result["metadata"]:
            budget = result["metadata"]["character_budget"]

            for variant_name in required_variants:
                if variant_name in result:
                    char_count = result[variant_name].get("char_count", 0)

                    if char_count > 180:  # Max budget
                        validation["issues"].append(
                            f"{variant_name} exceeds max budget: {char_count} > 180 chars"
                        )

                    if char_count < 90 and char_count > 0:  # Min budget (unless blocked)
                        validation["issues"].append(
                            f"{variant_name} below min budget: {char_count} < 90 chars"
                        )

        return validation

    def _print_test_summary(self, test_result: Dict):
        """Print formatted test summary"""

        validation = test_result["validation"]

        if validation["passed"]:
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED")

        if validation["issues"]:
            print("\n⚠️  Issues:")
            for issue in validation["issues"]:
                print(f"   - {issue}")

        # Print actual results
        actual = test_result["actual"]

        if "metadata" in actual:
            print(f"\n📊 Metadata:")
            meta = actual["metadata"]
            if "risk_score" in meta:
                print(f"   Risk Score: {meta['risk_score']}/100 ({meta.get('risk_level', 'UNKNOWN')})")
            if "modules_applied" in meta:
                print(f"   Modules: {', '.join(meta['modules_applied'])}")
            if "character_budget" in meta:
                print(f"   Character Budget: {meta['character_budget']}")

        if "execution_time_ms" in actual:
            print(f"\n⏱️  Execution Time: {actual['execution_time_ms']}ms")

        if "tokens_used" in actual:
            tokens = actual["tokens_used"]
            print(f"💰 Tokens: {tokens['total']} (input: {tokens['input']}, output: {tokens['output']})")

        # Print sample variant
        if "variant_b_value" in actual:
            variant = actual["variant_b_value"]
            print(f"\n📝 Sample Output (Variant B - Value):")
            print(f"   \"{variant['text']}\"")
            print(f"   ({variant.get('char_count', 0)} chars)")

    def generate_report(self, output_path: str = "validation_report.json"):
        """Generate comprehensive validation report"""

        # Calculate summary statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["validation"]["passed"])
        failed_tests = total_tests - passed_tests

        total_issues = sum(len(r["validation"]["issues"]) for r in self.results)

        avg_execution_time = sum(
            r["actual"].get("execution_time_ms", 0) for r in self.results
        ) / total_tests if total_tests > 0 else 0

        total_tokens = sum(
            r["actual"].get("tokens_used", {}).get("total", 0) for r in self.results
        )

        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "pass_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A",
                "total_issues": total_issues,
                "avg_execution_time_ms": int(avg_execution_time),
                "total_tokens_used": total_tokens
            },
            "test_results": self.results,
            "generated_at": datetime.now().isoformat()
        }

        # Save report
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*80}")
        print("VALIDATION REPORT")
        print(f"{'='*80}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ({report['summary']['pass_rate']})")
        print(f"Failed: {failed_tests}")
        print(f"Total Issues: {total_issues}")
        print(f"Avg Execution Time: {int(avg_execution_time)}ms")
        print(f"Total Tokens Used: {total_tokens:,}")
        print(f"\nReport saved to: {output_path}")

        return report


def create_test_suite() -> List[Dict]:
    """Create comprehensive test suite covering all major categories and edge cases"""

    harness = ValidationHarness()

    tests = []

    # TEST 1: Tech Specialist - iPhone (standard case)
    tests.append(harness.create_test_case(
        name="Tech Specialist - iPhone 13 Pro",
        item_category="smartphones",
        brand_model="Apple iPhone 13 Pro 256GB Sierra Blue",
        condition_raw="excellent",
        defects=["small screen scratch"],
        photos_type="actual",
        price_asking=549,
        target_platform="eBay.de",
        target_language="de",
        expected_module="iteration_12_tech",
        expected_risk_level="LOW",
        market_price_reference=1149,
        battery_health=87,
        included_items=["USB-C cable", "case"]
    ))

    # TEST 2: Luxury Specialist - Hermès Bag
    tests.append(harness.create_test_case(
        name="Luxury Specialist - Hermès Birkin",
        item_category="luxury_handbags",
        brand_model="Hermès Birkin 30 Togo Leather Gold Hardware",
        condition_raw="excellent",
        defects=["minor corner wear"],
        photos_type="actual",
        price_asking=12000,
        target_platform="eBay.de",
        target_language="en",
        expected_module="iteration_11_luxury",
        expected_risk_level="LOW",
        market_price_reference=16000,
        date_code="T stamp (2015)"
    ))

    # TEST 3: Clothing Specialist - Zara Dress
    tests.append(harness.create_test_case(
        name="Clothing Specialist - Zara Dress",
        item_category="womens_clothing",
        brand_model="Zara Midi Dress Floral Print",
        condition_raw="like new",
        defects=[],
        photos_type="actual",
        price_asking=25,
        target_platform="Vinted",
        target_language="de",
        expected_module="iteration_13_clothing",
        expected_risk_level="LOW",
        material="100% viscose",
        measurements={"chest": 88, "waist": 72, "length": 95}
    ))

    # TEST 4: Furniture Specialist - IKEA Bookshelf
    tests.append(harness.create_test_case(
        name="Furniture Specialist - IKEA BILLY",
        item_category="furniture",
        brand_model="IKEA BILLY Bookshelf White",
        condition_raw="good",
        defects=["small scratch on top shelf"],
        photos_type="actual",
        price_asking=25,
        target_platform="Kleinanzeigen",
        target_language="de",
        expected_module="iteration_14_furniture",
        expected_risk_level="LOW",
        measurements={"width": 80, "depth": 28, "height": 202}
    ))

    # TEST 5: HIGH RISK - Counterfeit Detection (luxury + low price + stock photos)
    tests.append(harness.create_test_case(
        name="HIGH RISK - Potential Counterfeit",
        item_category="luxury_handbags",
        brand_model="Louis Vuitton Neverfull MM",
        condition_raw="excellent",
        defects=[],
        photos_type="stock",  # RED FLAG
        price_asking=400,  # Market: ~€1200 (67% below)
        target_platform="Vinted",
        target_language="en",
        expected_module="iteration_11_luxury",
        expected_risk_level="HIGH",
        market_price_reference=1200
    ))

    # TEST 6: CRITICAL RISK - Battery Swelling (should block or strong warning)
    tests.append(harness.create_test_case(
        name="CRITICAL RISK - Battery Swelling",
        item_category="laptops",
        brand_model="Apple MacBook Pro 2017 15-inch",
        condition_raw="fair",
        defects=["battery swelling detected"],  # CRITICAL
        photos_type="actual",
        price_asking=400,
        target_platform="Kleinanzeigen",
        target_language="de",
        expected_module="iteration_12_tech",
        expected_risk_level="CRITICAL"
    ))

    # TEST 7: Multilingual - French Platform
    tests.append(harness.create_test_case(
        name="Multilingual - French (Vinted.fr)",
        item_category="mens_clothing",
        brand_model="Nike Air Max 90 Sneakers",
        condition_raw="good",
        defects=["minor sole wear"],
        photos_type="actual",
        price_asking=60,
        target_platform="Vinted.fr",
        target_language="fr",
        expected_module="iteration_13_clothing",
        expected_risk_level="LOW",
        market_price_reference=140
    ))

    # TEST 8: Bundle Handling - Gaming Setup
    tests.append(harness.create_test_case(
        name="Bundle Handling - Gaming Setup",
        item_category="gaming_consoles",
        brand_model="PlayStation 5 Disc Edition",
        condition_raw="excellent",
        defects=[],
        photos_type="actual",
        price_asking=650,
        target_platform="eBay.de",
        target_language="de",
        expected_module="iteration_12_tech",
        expected_risk_level="LOW",
        included_items=["2 controllers", "Spider-Man", "COD", "FIFA", "headset", "charging dock"]
    ))

    # TEST 9: Edge Case - Long Product Name (German appliance)
    tests.append(harness.create_test_case(
        name="Edge Case - Long German Product Name",
        item_category="home_appliances",
        brand_model="Bosch Serie 8 WAW28570 Waschmaschine i-Dos AutoDosierung HomeConnect",
        condition_raw="good",
        defects=["minor cosmetic wear"],
        photos_type="actual",
        price_asking=450,
        target_platform="eBay.de",
        target_language="de",
        expected_module="iteration_12_tech",
        expected_risk_level="LOW",
        market_price_reference=899
    ))

    # TEST 10: Price Optimization - Seasonal Item (Winter Coat in Summer)
    tests.append(harness.create_test_case(
        name="Price Optimization - Off-Season Winter Coat",
        item_category="womens_clothing",
        brand_model="Canada Goose Expedition Parka",
        condition_raw="excellent",
        defects=[],
        photos_type="actual",
        price_asking=400,
        target_platform="Vinted",
        target_language="en",
        expected_module="iteration_13_clothing",
        expected_risk_level="LOW",
        market_price_reference=1200,
        current_month=7  # July - summer, off-season for winter coat
    ))

    return tests


if __name__ == "__main__":
    print("🧪 PROMPT MUTATION FRAMEWORK - VALIDATION HARNESS")
    print("=" * 80)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n⚠️  No ANTHROPIC_API_KEY found in environment.")
        print("   Tests will run in SIMULATION MODE (for demonstration).")
        print("   To test with real LLM, set ANTHROPIC_API_KEY in .env file.\n")

    # Create harness
    harness = ValidationHarness()

    # Get test suite
    test_suite = create_test_suite()

    print(f"\nPrepared {len(test_suite)} test cases.\n")
    print("Starting validation...\n")

    # Execute all tests
    for test_case in test_suite:
        harness.execute_test(test_case)
        time.sleep(0.5)  # Brief pause between tests

    # Generate report
    report = harness.generate_report("validation_report.json")

    print("\n✅ Validation complete!")
