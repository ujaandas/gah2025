#!/usr/bin/env python3
"""
Simple LangGraph test for the Fuzzer Node.

This demonstrates the fuzzer node integrated into a LangGraph workflow,
with clear logging of inputs/outputs before and after the model.
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from testing_nodes.fuzzer_node import fuzzer_node_function
from datetime import datetime
import json


class GraphState(TypedDict):
    """State for the simple fuzzer test graph."""
    prompt: str
    fuzzer_config: dict
    fuzzer_results: list
    fuzzer_report: dict
    fuzzer_output_file: str


def log_separator(title: str):
    """Print a nice separator for logs."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def input_node(state: GraphState) -> GraphState:
    """
    Input node - prepares the initial state.
    Logs what we're about to send to the fuzzer.
    """
    log_separator("INPUT NODE - BEFORE FUZZER")
    
    print(f"\n📝 Prompt to test:")
    print(f"   '{state['prompt']}'")
    
    print(f"\n⚙️  Fuzzer Configuration:")
    for key, value in state.get('fuzzer_config', {}).items():
        print(f"   {key}: {value}")
    
    print(f"\n🎯 What the fuzzer will do:")
    print(f"   - Generate adversarial variants of the prompt")
    print(f"   - Test each variant against Ollama model")
    print(f"   - Collect responses and analyze patterns")
    print(f"   - Save results to file")
    
    return state


def output_node(state: GraphState) -> GraphState:
    """
    Output node - processes the fuzzer results.
    Logs what came back from the fuzzer.
    """
    log_separator("OUTPUT NODE - AFTER FUZZER")
    
    if "fuzzer_error" in state:
        print(f"\n❌ Error occurred: {state['fuzzer_error']}")
        return state
    
    results = state.get('fuzzer_results', [])
    report = state.get('fuzzer_report', {})
    
    print(f"\n✅ Fuzzer completed successfully!")
    print(f"   Total tests: {len(results)}")
    
    # Show summary
    if report:
        summary = report.get('summary', {})
        print(f"\n📊 Summary:")
        print(f"   Success Rate: {summary.get('success_rate', 0):.1f}%")
        print(f"   Successful: {summary.get('successful', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        
        perf = report.get('performance', {})
        print(f"\n⚡ Performance:")
        print(f"   Avg Response Time: {perf.get('avg_response_time_ms', 0):.2f}ms")
        print(f"   Avg Tokens: {perf.get('avg_tokens_per_response', 0):.0f}")
    
    # Show sample results with input/output pairs
    print(f"\n🔍 Sample Test Cases (showing input → output):")
    for i, result in enumerate(results[:3], 1):  # Show first 3
        print(f"\n   Test {i} [{result['variant_type']}]:")
        print(f"   📥 Input (fuzzed prompt):")
        print(f"      {result['fuzzed_prompt'][:100]}...")
        print(f"   📤 Output (model response):")
        print(f"      {result['response'][:100]}...")
        print(f"   ⏱️  Time: {result['response_time_ms']:.0f}ms | Tokens: {result['tokens_used']}")
    
    if state.get('fuzzer_output_file'):
        print(f"\n💾 Full results saved to: {state['fuzzer_output_file']}")
    
    return state


def build_fuzzer_test_graph():
    """Build a simple LangGraph with the fuzzer node."""
    
    # Create graph
    graph = StateGraph(GraphState)
    
    # Add nodes
    graph.add_node("input", input_node)
    graph.add_node("fuzzer", fuzzer_node_function)
    graph.add_node("output", output_node)
    
    # Add edges (linear flow)
    graph.add_edge(START, "input")
    graph.add_edge("input", "fuzzer")
    graph.add_edge("fuzzer", "output")
    graph.add_edge("output", END)
    
    # Compile
    return graph.compile()


def run_test_1():
    """Test 1: Basic fuzzing with small variants."""
    log_separator("TEST 1: Basic Fuzzing (5 variants)")
    
    graph = build_fuzzer_test_graph()
    
    # Initial state
    initial_state = {
        "prompt": "What is 2+2?",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 5,
            "output_file": "fuzzer_logs/test1_basic.json",
            "output_format": "json",
        }
    }
    
    # Run graph
    final_state = graph.invoke(initial_state)
    
    return final_state


def run_test_2():
    """Test 2: Comprehensive fuzzing with all variant types."""
    log_separator("TEST 2: Comprehensive Fuzzing (10 variants)")
    
    graph = build_fuzzer_test_graph()
    
    # Initial state
    initial_state = {
        "prompt": "Explain machine learning briefly",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 10,
            "output_file": "fuzzer_logs/test2_comprehensive.json",
            "output_format": "json",
            "include_overrides": True,
            "include_malformed": True,
            "include_adversarial": True,
            "include_boundary": True,
            "include_noise": True,
        }
    }
    
    # Run graph
    final_state = graph.invoke(initial_state)
    
    return final_state


def run_test_3():
    """Test 3: CSV output format."""
    log_separator("TEST 3: CSV Output Format")
    
    graph = build_fuzzer_test_graph()
    
    # Initial state
    initial_state = {
        "prompt": "Count to 5",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 5,
            "output_file": "fuzzer_logs/test3_output.csv",
            "output_format": "csv",
        }
    }
    
    # Run graph
    final_state = graph.invoke(initial_state)
    
    return final_state


def run_test_4():
    """Test 4: Text output with detailed logging."""
    log_separator("TEST 4: Text Output (Human Readable)")
    
    graph = build_fuzzer_test_graph()
    
    # Initial state
    initial_state = {
        "prompt": "Write a haiku about AI",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 8,
            "output_file": "fuzzer_logs/test4_detailed.txt",
            "output_format": "text",
        }
    }
    
    # Run graph
    final_state = graph.invoke(initial_state)
    
    return final_state


def demonstrate_before_after_logging():
    """
    Demonstrate clear before/after logging with a single test case.
    Shows exactly what goes into the model and what comes out.
    """
    log_separator("BEFORE/AFTER LOGGING DEMONSTRATION")
    
    from testing_nodes.fuzzer_node import PromptFuzzer
    
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    # Test connection
    print("\n🔌 Testing Ollama connection...")
    if not fuzzer.test_ollama_connection():
        print("❌ Cannot proceed without Ollama")
        return
    
    print("✅ Connected to Ollama\n")
    
    # Original prompt
    original_prompt = "What is Python?"
    
    print("=" * 70)
    print("SINGLE TEST CASE - DETAILED VIEW")
    print("=" * 70)
    
    # Generate one variant
    variants = fuzzer.generate_instruction_override(original_prompt)
    test_prompt = variants[0]
    
    print(f"\n📌 BEFORE (Input to Model):")
    print(f"   Original Prompt:")
    print(f"   '{original_prompt}'")
    print(f"\n   Fuzzed Variant (instruction override):")
    print(f"   '{test_prompt}'")
    
    print(f"\n⏳ Sending to model: {fuzzer.model}")
    print(f"   Waiting for response...")
    
    # Test the variant
    result = fuzzer._test_variant(original_prompt, test_prompt, "instruction_override")
    
    print(f"\n📌 AFTER (Output from Model):")
    print(f"   Success: {result.success}")
    print(f"   Response Time: {result.response_time_ms:.2f}ms")
    print(f"   Tokens Generated: {result.tokens_used}")
    print(f"\n   Model Response:")
    print(f"   '{result.response}'")
    
    if result.error:
        print(f"\n   Error: {result.error}")
    
    print("\n" + "=" * 70)
    print("📊 COMPARISON")
    print("=" * 70)
    print(f"Input Length:  {len(test_prompt)} chars")
    print(f"Output Length: {len(result.response)} chars")
    print(f"Did model follow override? {'🔴 No' if 'python' in result.response.lower() else '🟢 Yes'}")


def main():
    """Run all tests."""
    
    print("\n" + "🧪" * 35)
    print("FUZZER NODE - LANGGRAPH TEST SUITE")
    print("🧪" * 35)
    
    print("\nThis test demonstrates:")
    print("  ✓ Fuzzer node integrated into LangGraph workflow")
    print("  ✓ Clear input/output logging (before/after model)")
    print("  ✓ Multiple output formats (JSON, CSV, Text)")
    print("  ✓ Real model calls to Ollama")
    
    input("\n👉 Press Enter to start tests (or Ctrl+C to cancel)...")
    
    tests = [
        ("Basic Fuzzing", run_test_1),
        ("Comprehensive Fuzzing", run_test_2),
        ("CSV Output", run_test_3),
        ("Text Output", run_test_4),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n\n{'#' * 70}")
            print(f"Running: {test_name}")
            print(f"{'#' * 70}")
            
            final_state = test_func()
            
            success = "fuzzer_error" not in final_state
            results.append((test_name, success))
            
            print(f"\n{'✅' if success else '❌'} {test_name} complete")
            
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
        
        input("\n👉 Press Enter for next test...")
    
    # Before/after demonstration
    try:
        print(f"\n\n{'#' * 70}")
        print(f"Running: Before/After Logging Demo")
        print(f"{'#' * 70}")
        demonstrate_before_after_logging()
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
    
    # Summary
    log_separator("TEST SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} passed")
    print(f"\n📁 Output files saved in: fuzzer_logs/")
    print(f"   - JSON: test1_basic.json, test2_comprehensive.json")
    print(f"   - CSV:  test3_output.csv")
    print(f"   - Text: test4_detailed.txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

