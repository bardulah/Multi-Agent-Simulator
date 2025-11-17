"""
Standalone Validation Runner (Simulation Mode)
Runs validation tests without requiring API keys - demonstrates the test harness
"""

import json
import time
from datetime import datetime
from typing import Dict, List


class SimulatedValidator:
    """Simulated validation without external dependencies"""

    def __init__(self):
        self.results = []

    def execute_test(self, test_case: Dict) -> Dict:
        """Execute a single test case in simulation mode"""

        print(f"\n{'='*80}")
        print(f"TEST: {test_case['name']}")
        print(f"{'='*80}")

        start_time = time.time()

        # Simulate processing
        input_data = test_case["input"]
        expected = test_case["expected"]

        # Simulate routing logic
        modules_applied = self._route_to_module(input_data)

        # Simulate risk scoring
        risk_score, risk_level = self._calculate_risk(input_data)

        # Simulate character budget
        char_budget = self._calculate_budget(input_data, risk_level)

        # Simulate variant generation
        variants = self._generate_variants(input_data, char_budget)

        execution_time = int((time.time() - start_time) * 1000)

        result = {
            **variants,
            "metadata": {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "modules_applied": modules_applied,
                "character_budget": char_budget,
                "safety_warnings": self._generate_warnings(input_data, risk_level)
            },
            "execution_time_ms": execution_time,
            "simulated": True
        }

        # Validate
        validation = self._validate_result(result, expected)

        test_result = {
            "test_name": test_case["name"],
            "input": input_data,
            "expected": expected,
            "actual": result,
            "validation": validation,
            "timestamp": datetime.now().isoformat()
        }

        self.results.append(test_result)
        self._print_summary(test_result)

        return test_result

    def _route_to_module(self, input_data: Dict) -> List[str]:
        """Simulate module routing"""
        category = input_data["item_category"]
        price = input_data["price_asking"]

        modules = []

        # Primary routing
        if "luxury" in category or price > 1000:
            modules.append("iteration_11_luxury_specialist")
        elif category in ["smartphones", "laptops", "tablets", "gaming_consoles"]:
            modules.append("iteration_12_tech_specialist")
        elif "clothing" in category or "shoes" in category:
            modules.append("iteration_13_clothing_specialist")
        elif category == "furniture":
            modules.append("iteration_14_furniture_specialist")
        else:
            modules.append("base_framework_iterations_5-10")

        # Always apply pricing optimization
        modules.append("iteration_15_price_optimization")

        # Platform-specific
        modules.append(f"iteration_8_platform_{input_data['target_platform']}")

        # Multilingual
        modules.append(f"iteration_6_multilingual_{input_data['target_language']}")

        # Bundle handler if needed
        if len(input_data.get("included_items", [])) > 5:
            modules.append("iteration_7_bundle_handler")

        return modules

    def _calculate_risk(self, input_data: Dict) -> tuple:
        """Simulate risk scoring"""
        risk_score = 0

        # Counterfeit risk
        if ("luxury" in input_data["item_category"] and
            input_data.get("market_price_reference") and
            input_data["price_asking"] < input_data["market_price_reference"] * 0.6 and
            input_data["photos_type"] == "stock"):
            risk_score += 40

        # Safety defect risk
        defects = input_data.get("defects", [])
        critical_defects = ["battery swelling", "electrical smell", "overheating", "fire"]
        if any(critical in " ".join(defects).lower() for critical in critical_defects):
            risk_score += 50

        # Stolen goods risk
        if (input_data["item_category"] in ["smartphones", "laptops"] and
            input_data.get("market_price_reference") and
            input_data["price_asking"] < input_data["market_price_reference"] * 0.4):
            risk_score += 35

        # Photo mismatch risk
        if input_data["photos_type"] == "stock" and input_data["condition_raw"] != "mint":
            risk_score += 25

        # Determine level
        if risk_score >= 81:
            risk_level = "CRITICAL"
        elif risk_score >= 51:
            risk_level = "HIGH"
        elif risk_score >= 21:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return risk_score, risk_level

    def _calculate_budget(self, input_data: Dict, risk_level: str) -> int:
        """Simulate character budget calculation"""
        base_budget = 100

        # Language multiplier
        lang_multipliers = {
            "de": 1.25, "en": 1.0, "fr": 1.15, "it": 1.15,
            "es": 1.12, "nl": 1.22, "pl": 1.18
        }
        multiplier = lang_multipliers.get(input_data["target_language"], 1.0)
        budget = int(base_budget * multiplier)

        # Expansion rules
        if risk_level in ["HIGH", "CRITICAL"]:
            budget += 50
        if input_data["item_category"] in ["luxury_handbags", "luxury_watches"]:
            budget += 30
        if len(input_data.get("defects", [])) > 2:
            budget += 25
        if input_data["target_platform"] == "eBay.de":
            budget += 20
        if input_data["price_asking"] > 500:
            budget += 15

        # Constraints
        return min(max(budget, 90), 180)

    def _generate_variants(self, input_data: Dict, char_budget: int) -> Dict:
        """Simulate variant generation"""
        brand = input_data["brand_model"].split()[0]
        price = input_data["price_asking"]
        condition = "★★★★" if "excellent" in input_data["condition_raw"].lower() else "★★★"
        photo = "📸" if input_data["photos_type"] == "actual" else "🖼️"

        # Different variants based on optimization
        variant_a = f"Great find{photo} {brand}{condition} €{price}"
        variant_b = f"Save big! {brand}{photo}{condition} €{price}"
        variant_c = f"Verified{photo} {brand}{condition} €{price}"

        return {
            "variant_a_emotion": {
                "text": variant_a,
                "char_count": len(variant_a),
                "optimization_focus": "Emotional appeal"
            },
            "variant_b_value": {
                "text": variant_b,
                "char_count": len(variant_b),
                "optimization_focus": "Price value"
            },
            "variant_c_trust": {
                "text": variant_c,
                "char_count": len(variant_c),
                "optimization_focus": "Trust signals"
            }
        }

    def _generate_warnings(self, input_data: Dict, risk_level: str) -> List[str]:
        """Generate safety warnings"""
        warnings = []

        if risk_level == "CRITICAL":
            defects = input_data.get("defects", [])
            if any("battery" in d.lower() for d in defects):
                warnings.append("⚠️ CRITICAL: Battery safety hazard - professional assessment required")

        if risk_level == "HIGH":
            if input_data["photos_type"] == "stock":
                warnings.append("⚠️ Stock photos only - authentication recommended")

        return warnings

    def _validate_result(self, result: Dict, expected: Dict) -> Dict:
        """Validate result against expectations"""
        validation = {"passed": True, "issues": []}

        # Check module routing
        applied = result["metadata"]["modules_applied"]
        expected_module = expected["module"]

        if not any(expected_module in module for module in applied):
            validation["passed"] = False
            validation["issues"].append(
                f"Module routing failed: expected '{expected_module}', got {applied}"
            )

        # Check risk level
        actual_risk = result["metadata"]["risk_level"]
        expected_risk = expected["risk_level"]

        if actual_risk != expected_risk:
            validation["issues"].append(
                f"Risk level mismatch: expected '{expected_risk}', got '{actual_risk}'"
            )

        # Check variants
        for variant_key in ["variant_a_emotion", "variant_b_value", "variant_c_trust"]:
            if variant_key not in result:
                validation["passed"] = False
                validation["issues"].append(f"Missing variant: {variant_key}")

        # Check character budget
        budget = result["metadata"]["character_budget"]
        if budget < 90 or budget > 180:
            validation["passed"] = False
            validation["issues"].append(f"Character budget out of range: {budget}")

        return validation

    def _print_summary(self, test_result: Dict):
        """Print test summary"""
        validation = test_result["validation"]
        actual = test_result["actual"]

        if validation["passed"]:
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED")

        if validation["issues"]:
            print("\n⚠️  Issues:")
            for issue in validation["issues"]:
                print(f"   - {issue}")

        # Print metadata
        meta = actual["metadata"]
        print(f"\n📊 Metadata:")
        print(f"   Risk Score: {meta['risk_score']}/100 ({meta['risk_level']})")
        print(f"   Modules: {', '.join(meta['modules_applied'][:3])}...")
        print(f"   Character Budget: {meta['character_budget']}")

        if meta["safety_warnings"]:
            print(f"\n⚠️  Safety Warnings:")
            for warning in meta["safety_warnings"]:
                print(f"   {warning}")

        # Print sample variant
        variant = actual["variant_b_value"]
        print(f"\n📝 Sample Output (Variant B):")
        print(f"   \"{variant['text']}\"")
        print(f"   ({variant['char_count']} chars, {variant['optimization_focus']})")

        print(f"\n⏱️  Execution Time: {actual['execution_time_ms']}ms (simulated)")

    def generate_report(self) -> Dict:
        """Generate validation report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["validation"]["passed"])
        failed = total - passed

        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "N/A",
                "total_issues": sum(len(r["validation"]["issues"]) for r in self.results),
                "simulation_mode": True
            },
            "test_results": self.results,
            "generated_at": datetime.now().isoformat()
        }

        # Save report
        with open("validation_report_simulation.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n{'='*80}")
        print("VALIDATION REPORT (SIMULATION MODE)")
        print(f"{'='*80}")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ({report['summary']['pass_rate']})")
        print(f"Failed: {failed}")
        print(f"Total Issues: {report['summary']['total_issues']}")
        print(f"\nReport saved to: validation_report_simulation.json")

        return report


def create_test_cases() -> List[Dict]:
    """Create test suite"""

    tests = []

    # TEST 1: Tech Specialist - iPhone
    tests.append({
        "name": "Tech Specialist - iPhone 13 Pro",
        "input": {
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
        },
        "expected": {
            "module": "iteration_12_tech",
            "risk_level": "LOW"
        }
    })

    # TEST 2: Luxury Specialist - Hermès
    tests.append({
        "name": "Luxury Specialist - Hermès Birkin",
        "input": {
            "item_category": "luxury_handbags",
            "brand_model": "Hermès Birkin 30 Togo Leather",
            "condition_raw": "excellent",
            "defects": ["minor corner wear"],
            "photos_type": "actual",
            "price_asking": 12000,
            "target_platform": "eBay.de",
            "target_language": "en",
            "market_price_reference": 16000
        },
        "expected": {
            "module": "iteration_11_luxury",
            "risk_level": "LOW"
        }
    })

    # TEST 3: HIGH RISK - Potential Counterfeit
    tests.append({
        "name": "HIGH RISK - Potential Counterfeit",
        "input": {
            "item_category": "luxury_handbags",
            "brand_model": "Louis Vuitton Neverfull MM",
            "condition_raw": "excellent",
            "defects": [],
            "photos_type": "stock",  # RED FLAG
            "price_asking": 400,
            "target_platform": "Vinted",
            "target_language": "en",
            "market_price_reference": 1200  # 67% below market
        },
        "expected": {
            "module": "iteration_11_luxury",
            "risk_level": "HIGH"
        }
    })

    # TEST 4: CRITICAL RISK - Battery Swelling
    tests.append({
        "name": "CRITICAL RISK - Battery Swelling",
        "input": {
            "item_category": "laptops",
            "brand_model": "Apple MacBook Pro 2017",
            "condition_raw": "fair",
            "defects": ["battery swelling detected"],  # CRITICAL
            "photos_type": "actual",
            "price_asking": 400,
            "target_platform": "Kleinanzeigen",
            "target_language": "de"
        },
        "expected": {
            "module": "iteration_12_tech",
            "risk_level": "CRITICAL"
        }
    })

    # TEST 5: Clothing Specialist
    tests.append({
        "name": "Clothing Specialist - Zara Dress",
        "input": {
            "item_category": "womens_clothing",
            "brand_model": "Zara Midi Dress Floral",
            "condition_raw": "like new",
            "defects": [],
            "photos_type": "actual",
            "price_asking": 25,
            "target_platform": "Vinted",
            "target_language": "de"
        },
        "expected": {
            "module": "iteration_13_clothing",
            "risk_level": "LOW"
        }
    })

    # TEST 6: Furniture Specialist
    tests.append({
        "name": "Furniture Specialist - IKEA BILLY",
        "input": {
            "item_category": "furniture",
            "brand_model": "IKEA BILLY Bookshelf White",
            "condition_raw": "good",
            "defects": ["small scratch"],
            "photos_type": "actual",
            "price_asking": 25,
            "target_platform": "Kleinanzeigen",
            "target_language": "de"
        },
        "expected": {
            "module": "iteration_14_furniture",
            "risk_level": "LOW"
        }
    })

    # TEST 7: Bundle Handling
    tests.append({
        "name": "Bundle Handling - Gaming Setup",
        "input": {
            "item_category": "gaming_consoles",
            "brand_model": "PlayStation 5 Disc Edition",
            "condition_raw": "excellent",
            "defects": [],
            "photos_type": "actual",
            "price_asking": 650,
            "target_platform": "eBay.de",
            "target_language": "de",
            "included_items": ["controller 1", "controller 2", "Spider-Man", "COD", "FIFA", "headset"]
        },
        "expected": {
            "module": "iteration_12_tech",
            "risk_level": "LOW"
        }
    })

    # TEST 8: Multilingual - French
    tests.append({
        "name": "Multilingual - French Platform",
        "input": {
            "item_category": "mens_clothing",
            "brand_model": "Nike Air Max 90",
            "condition_raw": "good",
            "defects": ["minor sole wear"],
            "photos_type": "actual",
            "price_asking": 60,
            "target_platform": "Vinted.fr",
            "target_language": "fr",
            "market_price_reference": 140
        },
        "expected": {
            "module": "iteration_13_clothing",
            "risk_level": "LOW"
        }
    })

    return tests


if __name__ == "__main__":
    print("🧪 PROMPT MUTATION FRAMEWORK - VALIDATION (SIMULATION MODE)")
    print("="*80)
    print("\nℹ️  Running in simulation mode (no API required)")
    print("   This demonstrates the validation framework logic.\n")

    validator = SimulatedValidator()
    test_suite = create_test_cases()

    print(f"Prepared {len(test_suite)} test cases.\n")

    for test in test_suite:
        validator.execute_test(test)
        time.sleep(0.2)

    report = validator.generate_report()

    print("\n✅ Validation simulation complete!")
    print("\nTo run with real LLM:")
    print("1. Install dependencies: pip install anthropic python-dotenv")
    print("2. Set ANTHROPIC_API_KEY in .env file")
    print("3. Run: python validation_harness.py")
