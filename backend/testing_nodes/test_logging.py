#!/usr/bin/env python3
"""
Test script for fuzzer logging functionality.

Demonstrates saving fuzzer results to different file formats.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from testing_nodes.fuzzer_node import PromptFuzzer, fuzzer_node_function


def test_json_logging():
    """Test saving results as JSON."""
    print("\n" + "=" * 70)
    print("TEST 1: Save Results as JSON")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    # Test connection
    if not fuzzer.test_ollama_connection():
        print("❌ Cannot proceed without Ollama")
        return False
    
    # Run fuzzing
    print("\n🔬 Running fuzzing...")
    results = fuzzer.fuzz_prompt(
        prompt="What is machine learning?",
        max_variants=5
    )
    
    # Save to JSON
    output_file = "test_outputs/fuzzer_results.json"
    success = fuzzer.save_results_to_file(output_file, format="json")
    
    if success:
        print(f"\n📄 Check the file: {output_file}")
        print(f"   Contains: {len(results)} test results + analysis")
        return True
    return False


def test_csv_logging():
    """Test saving results as CSV."""
    print("\n" + "=" * 70)
    print("TEST 2: Save Results as CSV")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    if not fuzzer.test_ollama_connection():
        print("❌ Cannot proceed without Ollama")
        return False
    
    # Run fuzzing
    print("\n🔬 Running fuzzing...")
    results = fuzzer.fuzz_prompt(
        prompt="Explain neural networks briefly",
        max_variants=5
    )
    
    # Save to CSV
    output_file = "test_outputs/fuzzer_results.csv"
    success = fuzzer.save_results_to_file(output_file, format="csv")
    
    if success:
        print(f"\n📊 Check the file: {output_file}")
        print(f"   Contains: {len(results)} rows (great for spreadsheets!)")
        return True
    return False


def test_text_logging():
    """Test saving results as text."""
    print("\n" + "=" * 70)
    print("TEST 3: Save Results as Text")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    if not fuzzer.test_ollama_connection():
        print("❌ Cannot proceed without Ollama")
        return False
    
    # Run fuzzing
    print("\n🔬 Running fuzzing...")
    results = fuzzer.fuzz_prompt(
        prompt="What is deep learning?",
        max_variants=5
    )
    
    # Save to text
    output_file = "test_outputs/fuzzer_results.txt"
    success = fuzzer.save_results_to_file(output_file, format="text")
    
    if success:
        print(f"\n📝 Check the file: {output_file}")
        print(f"   Contains: Formatted report (human-readable)")
        return True
    return False


def test_append_mode():
    """Test appending results to existing files."""
    print("\n" + "=" * 70)
    print("TEST 4: Append Mode (Multiple Runs)")
    print("=" * 70)
    
    output_file = "test_outputs/fuzzer_history.json"
    
    # Run 1
    print("\n📝 Run 1: Initial test")
    fuzzer1 = PromptFuzzer(model="gemma3:4b")
    if not fuzzer1.test_ollama_connection():
        return False
    
    fuzzer1.fuzz_prompt("Test prompt 1", max_variants=3)
    fuzzer1.save_results_to_file(output_file, format="json", append=False)
    
    # Run 2
    print("\n📝 Run 2: Appending to existing file")
    fuzzer2 = PromptFuzzer(model="gemma3:4b")
    fuzzer2.fuzz_prompt("Test prompt 2", max_variants=3)
    fuzzer2.save_results_to_file(output_file, format="json", append=True)
    
    print(f"\n✅ Both runs saved to: {output_file}")
    print(f"   File now contains results from 2 separate fuzzing sessions!")
    return True


def test_langgraph_with_logging():
    """Test LangGraph integration with file logging."""
    print("\n" + "=" * 70)
    print("TEST 5: LangGraph Integration with Logging")
    print("=" * 70)
    
    state = {
        "prompt": "Explain supervised learning",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 5,
            "output_file": "test_outputs/langgraph_fuzzer.json",
            "output_format": "json",
            "append_results": False,
        }
    }
    
    print("\n🚀 Running fuzzer via LangGraph node function...")
    result = fuzzer_node_function(state)
    
    if "fuzzer_error" in result:
        print(f"❌ Error: {result['fuzzer_error']}")
        return False
    
    print(f"\n✅ Success!")
    print(f"   Tests run: {len(result['fuzzer_results'])}")
    print(f"   Saved to: {result.get('fuzzer_output_file', 'N/A')}")
    
    # Show summary
    report = result['fuzzer_report']
    print(f"\n📊 Quick Stats:")
    print(f"   Success Rate: {report['summary']['success_rate']:.1f}%")
    print(f"   Avg Response Time: {report['performance']['avg_response_time_ms']:.2f}ms")
    
    return True


def test_all_formats_same_data():
    """Save the same data in all three formats for comparison."""
    print("\n" + "=" * 70)
    print("TEST 6: Same Data, All Formats")
    print("=" * 70)
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    if not fuzzer.test_ollama_connection():
        return False
    
    # Run fuzzing once
    print("\n🔬 Running fuzzing...")
    prompt = "What are the types of machine learning?"
    fuzzer.fuzz_prompt(prompt, max_variants=8)
    
    # Save in all formats
    print("\n💾 Saving in multiple formats...")
    fuzzer.save_results_to_file("test_outputs/comparison.json", format="json")
    fuzzer.save_results_to_file("test_outputs/comparison.csv", format="csv")
    fuzzer.save_results_to_file("test_outputs/comparison.txt", format="text")
    
    print("\n✅ Same data saved in 3 formats:")
    print("   📄 comparison.json - For programmatic access")
    print("   📊 comparison.csv  - For Excel/spreadsheet analysis")
    print("   📝 comparison.txt  - For human reading")
    
    return True


def run_all_tests():
    """Run all logging tests."""
    print("\n" + "🧪" * 35)
    print("FUZZER LOGGING TEST SUITE")
    print("🧪" * 35)
    
    tests = [
        ("JSON Logging", test_json_logging),
        ("CSV Logging", test_csv_logging),
        ("Text Logging", test_text_logging),
        ("Append Mode", test_append_mode),
        ("LangGraph Integration", test_langgraph_with_logging),
        ("All Formats Comparison", test_all_formats_same_data),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        print("\n📁 Output files created in: test_outputs/")
        print("   Check these files to see the different formats!")
    
    return passed, total - passed


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Fuzzer Logging")
    parser.add_argument(
        "--test",
        type=int,
        choices=range(1, 7),
        help="Run a specific test (1-6)",
    )
    
    args = parser.parse_args()
    
    if args.test:
        test_map = {
            1: test_json_logging,
            2: test_csv_logging,
            3: test_text_logging,
            4: test_append_mode,
            5: test_langgraph_with_logging,
            6: test_all_formats_same_data,
        }
        print(f"\n🎯 Running Test {args.test}...\n")
        success = test_map[args.test]()
        sys.exit(0 if success else 1)
    else:
        # Run all tests
        passed, failed = run_all_tests()
        sys.exit(0 if failed == 0 else 1)

