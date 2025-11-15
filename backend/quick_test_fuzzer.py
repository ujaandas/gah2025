#!/usr/bin/env python3
"""
Quick test of the Fuzzer Node in a LangGraph workflow.
Non-interactive version for automated testing.
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from testing_nodes.fuzzer_node import fuzzer_node_function


class GraphState(TypedDict):
    """State for the fuzzer test graph."""
    prompt: str
    fuzzer_config: dict
    fuzzer_results: list
    fuzzer_report: dict


def log_input(state: GraphState) -> GraphState:
    """Log what's going into the fuzzer."""
    print("\n" + "=" * 70)
    print("📥 INPUT TO FUZZER")
    print("=" * 70)
    print(f"\nPrompt: '{state['prompt']}'")
    print(f"\nConfig:")
    for key, value in state.get('fuzzer_config', {}).items():
        print(f"  {key}: {value}")
    print("\n⏳ Running fuzzer...")
    return state


def log_output(state: GraphState) -> GraphState:
    """Log what came out of the fuzzer."""
    print("\n" + "=" * 70)
    print("📤 OUTPUT FROM FUZZER")
    print("=" * 70)
    
    if "fuzzer_error" in state:
        print(f"\n❌ Error: {state['fuzzer_error']}")
        return state
    
    results = state.get('fuzzer_results', [])
    report = state.get('fuzzer_report', {})
    
    print(f"\n✅ Tests completed: {len(results)}")
    
    if report:
        summary = report.get('summary', {})
        print(f"\n📊 Success Rate: {summary.get('success_rate', 0):.1f}%")
        print(f"   Successful: {summary.get('successful', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
    
    # Show 2 example input/output pairs
    print(f"\n🔍 Example Test Cases:")
    for i, result in enumerate(results[:2], 1):
        print(f"\n  Test {i} ({result['variant_type']}):")
        print(f"    📥 IN:  {result['fuzzed_prompt'][:80]}...")
        print(f"    📤 OUT: {result['response'][:80]}...")
        print(f"    ⏱️  {result['response_time_ms']:.0f}ms | {result['tokens_used']} tokens")
    
    if state.get('fuzzer_output_file'):
        print(f"\n💾 Saved to: {state['fuzzer_output_file']}")
    
    return state


def main():
    """Run a quick fuzzer test."""
    
    print("\n" + "🧪" * 35)
    print("QUICK FUZZER TEST - LangGraph Integration")
    print("🧪" * 35)
    
    # Build graph
    graph = StateGraph(GraphState)
    graph.add_node("log_input", log_input)
    graph.add_node("fuzzer", fuzzer_node_function)
    graph.add_node("log_output", log_output)
    
    graph.add_edge(START, "log_input")
    graph.add_edge("log_input", "fuzzer")
    graph.add_edge("fuzzer", "log_output")
    graph.add_edge("log_output", END)
    
    compiled_graph = graph.compile()
    
    # Test state
    initial_state = {
        "prompt": "What is 2+2?",
        "fuzzer_config": {
            "model": "llama3.2:latest",
            "max_variants": 5,
            "output_file": "fuzzer_logs/quick_test.json",
            "output_format": "json",
        }
    }
    
    # Run
    print("\n🚀 Starting fuzzer workflow...")
    final_state = compiled_graph.invoke(initial_state)
    
    # Final summary
    print("\n" + "=" * 70)
    print("✨ WORKFLOW COMPLETE")
    print("=" * 70)
    
    if "fuzzer_error" not in final_state:
        print("\n✅ All tests passed!")
        output_file = final_state.get('fuzzer_output_file')
        if output_file:
            print(f"📁 Results saved to: {output_file}")
        else:
            print("📁 Results logged to terminal only")
    else:
        print(f"\n❌ Workflow failed: {final_state.get('fuzzer_error')}")
    
    return final_state


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

