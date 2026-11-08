"""
KisanSamvaad - Master Automated Test Runner
Executes all 10 test suites covering Sarvam handling, speech workflow, soil card validation,
agricultural RAG, banned chemical rejection, restricted dosage, Mandi freshness,
weather validation, API error handling, and end-to-end integration.
"""

import unittest
import sys
import os
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

# Import all 10 test suites
from tests.test_1_sarvam_handling import TestSarvamHandling
from tests.test_2_speech_workflow import TestSpeechWorkflow
from tests.test_3_soil_card_validation import TestSoilCardValidation
from tests.test_4_agricultural_rag import TestAgriculturalRAG
from tests.test_5_banned_chemicals import TestBannedChemicals
from tests.test_6_restricted_dosage import TestRestrictedDosage
from tests.test_7_mandi_freshness import TestMandiFreshness
from tests.test_8_weather_validation import TestWeatherValidation
from tests.test_9_api_error_handling import TestAPIErrorHandling
from tests.test_10_e2e_integration import TestEndToEndIntegration

def run_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suites = [
        ("1. Sarvam Handling & Fallback", TestSarvamHandling),
        ("2. Speech Workflow & Synthesis", TestSpeechWorkflow),
        ("3. Soil Card Validation & Remediation", TestSoilCardValidation),
        ("4. Agricultural RAG & Provenance", TestAgriculturalRAG),
        ("5. Banned Chemical Fail-Closed Guardrails", TestBannedChemicals),
        ("6. Restricted Agrochemical Dosages", TestRestrictedDosage),
        ("7. Mandi Data Freshness & Transparency", TestMandiFreshness),
        ("8. Agricultural Weather & Spray Windows", TestWeatherValidation),
        ("9. API Error Handling & Resilience", TestAPIErrorHandling),
        ("10. End-to-End Multilingual Pipeline", TestEndToEndIntegration)
    ]

    print("\n" + "="*70)
    print("🌾 KISANSAMVAAD MASTER TEST SUITE - 10 CRITICAL SPECIFICATION AREAS")
    print("="*70 + "\n")

    overall_passed = True
    total_tests_run = 0
    start_time = time.time()

    for title, test_class in suites:
        class_suite = loader.loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=0)
        res = runner.run(class_suite)
        total_tests_run += res.testsRun

        if res.wasSuccessful():
            print(f"  [PASSED] Suite {title} ({res.testsRun} tests)")
        else:
            overall_passed = False
            print(f"  [FAILED] Suite {title} ({len(res.failures)} failures, {len(res.errors)} errors)")
            for failure in res.failures:
                print(f"     -> Failure in {failure[0]}: {failure[1][:120]}...")
            for error in res.errors:
                print(f"     -> Error in {error[0]}: {error[1][:120]}...")

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "="*70)
    if overall_passed:
        print(f"✅ ALL {total_tests_run} VERIFICATION TESTS PASSED SUCCESSFULLY! ({elapsed}s)")
    else:
        print(f"❌ TEST SUITE RUN COMPLETED WITH FAILURES ({elapsed}s)")
    print("="*70 + "\n")

    return 0 if overall_passed else 1

if __name__ == "__main__":
    sys.exit(run_suite())

