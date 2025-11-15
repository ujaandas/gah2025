"""
Test script for fuzzer_node.py

This script tests the Fuzzer Node functionality with various scenarios.
Make sure Ollama is running with: ollama serve
And the model is pulled: ollama pull gemma2:2b
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from testing_nodes.fuzzer_node import (
    PromptFuzzer,
    fuzzer_node_function,
    FuzzResult
)


def test_ollama_connection():
    """Test 1: Check Ollama connection."""
    print("\n" + "=" * 70)
    print("TEST 1: Ollama Connection")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    if fuzzer.test_ollama_connection():
        print("✅ Ollama connection successful!")
        return True
    else:
        print("❌ Ollama connection failed!")
        print("\n💡 Setup instructions:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Pull model: ollama pull gemma2:2b")
        return False


def test_prompt_generation():
    """Test 2: Test prompt variant generation (no LLM calls)."""
    print("\n" + "=" * 70)
    print("TEST 2: Prompt Variant Generation")
    print("=" * 70)
    
    fuzzer = PromptFuzzer()
    test_prompt = "What is the capital of France?"
    
    # Test each generator
    print("\n📝 Instruction Override Variants:")
    overrides = fuzzer.generate_instruction_override(test_prompt)
    print(f"   Generated {len(overrides)} variants")
    print(f"   Example: {overrides[0][:80]}...")
    
    print("\n📝 Malformed Input Variants:")
    malformed = fuzzer.generate_malformed_inputs(test_prompt)
    print(f"   Generated {len(malformed)} variants")
    print(f"   Example (empty): '{malformed[0]}'")
    print(f"   Example (long): {len(malformed[5])} chars")
    
    print("\n📝 Adversarial Variants:")
    adversarial = fuzzer.generate_adversarial_prompts(test_prompt)
    print(f"   Generated {len(adversarial)} variants")
    print(f"   Example: {adversarial[0][:80]}...")
    
    print("\n📝 Boundary Test Variants:")
    boundary = fuzzer.generate_boundary_tests(test_prompt)
    print(f"   Generated {len(boundary)} variants")
    print(f"   Example: {boundary[0][:80]}...")
    
    print("\n📝 Noise Variants:")
    noise = fuzzer.generate_noise_variants(test_prompt)
    print(f"   Generated {len(noise)} variants")
    print(f"   Example: {noise[0][:80]}...")
    
    total = len(overrides) + len(malformed) + len(adversarial) + len(boundary) + len(noise)
    print(f"\n✅ Total variants that can be generated: {total}")
    return True


def test_basic_fuzzing():
    """Test 3: Basic fuzzing with a simple prompt."""
    print("\n" + "=" * 70)
    print("TEST 3: Basic Fuzzing (5 variants)")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    # Test with just a few variants
    results = fuzzer.fuzz_prompt(
        prompt="Say hello",
        max_variants=5,
        include_overrides=True,
        include_malformed=False,
        include_adversarial=False,
        include_boundary=False,
        include_noise=False
    )
    
    print(f"\n📊 Results:")
    print(f"   Total tests: {len(results)}")
    print(f"   Successful: {sum(1 for r in results if r.success)}")
    print(f"   Failed: {sum(1 for r in results if not r.success)}")
    
    # Show a sample result
    if results and results[0].success:
        print(f"\n💬 Sample Response:")
        print(f"   Variant Type: {results[0].variant_type}")
        print(f"   Prompt: {results[0].fuzzed_prompt[:80]}...")
        print(f"   Response: {results[0].response[:150]}...")
        print(f"   Response Time: {results[0].response_time_ms:.2f}ms")
    
    print("\n✅ Basic fuzzing test complete!")
    return len(results) > 0


def test_comprehensive_fuzzing():
    """Test 4: Comprehensive fuzzing with all variant types."""
    print("\n" + "=" * 70)
    print("TEST 4: Comprehensive Fuzzing (20 variants)")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    # Test with more variants across all types
    results = fuzzer.fuzz_prompt(
        prompt="Explain machine learning in one sentence",
        max_variants=20,
        include_overrides=True,
        include_malformed=True,
        include_adversarial=True,
        include_boundary=True,
        include_noise=True
    )
    
    # Print the full report
    fuzzer.print_report()
    
    print("\n✅ Comprehensive fuzzing test complete!")
    return len(results) > 0


def test_langgraph_integration():
    """Test 5: Test integration with LangGraph state."""
    print("\n" + "=" * 70)
    print("TEST 5: LangGraph Node Function Integration")
    print("=" * 70)
    
    # Simulate a LangGraph state
    state = {
        "prompt": "What is 2+2?",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 10,
            "include_overrides": True,
            "include_malformed": True,
            "include_adversarial": False,
            "include_boundary": False,
            "include_noise": False,
        }
    }
    
    print(f"\n📋 Input State:")
    print(f"   Prompt: {state['prompt']}")
    print(f"   Max Variants: {state['fuzzer_config']['max_variants']}")
    
    # Run the node function
    result = fuzzer_node_function(state)
    
    print(f"\n📊 Output State:")
    if "fuzzer_error" in result:
        print(f"   ❌ Error: {result['fuzzer_error']}")
        return False
    else:
        print(f"   ✅ Fuzzer Results: {len(result['fuzzer_results'])} tests")
        print(f"   ✅ Report Generated: {bool(result['fuzzer_report'])}")
        
        report = result['fuzzer_report']
        print(f"\n📈 Quick Stats:")
        print(f"   Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"   Avg Response Time: {report['performance']['avg_response_time_ms']:.2f}ms")
        
        return True


def test_error_handling():
    """Test 6: Test error handling with invalid inputs."""
    print("\n" + "=" * 70)
    print("TEST 6: Error Handling")
    print("=" * 70)
    
    print("\n📝 Test 6a: Empty prompt")
    state = {"prompt": ""}
    result = fuzzer_node_function(state)
    if "fuzzer_error" in result:
        print(f"   ✅ Correctly caught error: {result['fuzzer_error']}")
    else:
        print(f"   ❌ Should have caught empty prompt error")
    
    print("\n📝 Test 6b: Missing prompt")
    state = {"fuzzer_config": {"model": "gemma2:2b"}}
    result = fuzzer_node_function(state)
    if "fuzzer_error" in result:
        print(f"   ✅ Correctly caught error: {result['fuzzer_error']}")
    else:
        print(f"   ❌ Should have caught missing prompt error")
    
    print("\n📝 Test 6c: Invalid model name")
    fuzzer = PromptFuzzer(model="nonexistent-model-xyz")
    if not fuzzer.test_ollama_connection():
        print(f"   ✅ Correctly detected invalid model")
    else:
        print(f"   ⚠️  Model might exist or connection check passed unexpectedly")
    
    print("\n✅ Error handling tests complete!")
    return True


def test_analysis_features():
    """Test 7: Test analysis and reporting features."""
    print("\n" + "=" * 70)
    print("TEST 7: Analysis & Reporting")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    # Generate some test results
    print("\n📝 Running fuzzing to generate data...")
    results = fuzzer.fuzz_prompt(
        prompt="Count to 5",
        max_variants=8,
        include_overrides=True,
        include_malformed=True,
        include_adversarial=False,
        include_boundary=False,
        include_noise=False
    )
    
    print("\n📊 Testing analysis functions...")
    
    # Test to_dict conversion
    if results:
        result_dict = results[0].to_dict()
        print(f"   ✅ FuzzResult.to_dict() works")
        print(f"      Keys: {list(result_dict.keys())}")
    
    # Test analyze_results
    report = fuzzer.analyze_results()
    print(f"\n   ✅ analyze_results() works")
    print(f"      Report sections: {list(report.keys())}")
    
    # Test print_report
    print(f"\n   ✅ Generating formatted report...")
    fuzzer.print_report()
    
    print("\n✅ Analysis features test complete!")
    return True


def run_all_tests():
    """Run all tests in sequence."""
    print("\n" + "🧪" * 35)
    print("FUZZER NODE TEST SUITE")
    print("🧪" * 35)
    
    tests = [
        ("Connection Test", test_ollama_connection),
        ("Variant Generation", test_prompt_generation),
        ("Basic Fuzzing", test_basic_fuzzing),
        ("Comprehensive Fuzzing", test_comprehensive_fuzzing),
        ("LangGraph Integration", test_langgraph_integration),
        ("Error Handling", test_error_handling),
        ("Analysis Features", test_analysis_features),
    ]
    
    results = []
    
    # Run connection test first - if it fails, skip LLM tests
    connection_ok = test_ollama_connection()
    
    if not connection_ok:
        print("\n⚠️  Skipping LLM-dependent tests (tests 3-7)")
        print("   Running only variant generation test...")
        results.append(("Connection Test", False))
        results.append(("Variant Generation", test_prompt_generation()))
        # Mark remaining tests as skipped
        for test_name, _ in tests[2:]:
            results.append((test_name, None))  # None = skipped
    else:
        results.append(("Connection Test", True))
        
        # Run remaining tests
        for test_name, test_func in tests[1:]:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"\n❌ Test '{test_name}' crashed with error: {e}")
                results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    total = len(results)
    
    for test_name, result in results:
        if result is True:
            print(f"✅ {test_name}")
        elif result is False:
            print(f"❌ {test_name}")
        else:
            print(f"⏭️  {test_name} (skipped)")
    
    print(f"\n📊 Results: {passed}/{total} passed, {failed} failed, {skipped} skipped")
    
    if not connection_ok:
        print("\n💡 To run all tests, make sure Ollama is running:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Pull model: ollama pull gemma2:2b")
        print("   3. Run tests again: python test_fuzzer.py")
    
    return passed, failed, skipped


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the Fuzzer Node")
    parser.add_argument(
        "--test",
        type=int,
        choices=range(1, 8),
        help="Run a specific test (1-7)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run only quick tests (no LLM calls)",
    )
    
    args = parser.parse_args()
    
    if args.quick:
        print("\n🏃 Running quick tests only (no LLM calls)...\n")
        test_prompt_generation()
        test_error_handling()
    elif args.test:
        test_map = {
            1: test_ollama_connection,
            2: test_prompt_generation,
            3: test_basic_fuzzing,
            4: test_comprehensive_fuzzing,
            5: test_langgraph_integration,
            6: test_error_handling,
            7: test_analysis_features,
        }
        print(f"\n🎯 Running Test {args.test}...\n")
        test_map[args.test]()
    else:
        # Run all tests
        passed, failed, skipped = run_all_tests()
        
        # Exit with appropriate code
        if failed > 0:
            sys.exit(1)
        elif passed == 0:
            sys.exit(2)
        else:
            sys.exit(0)

