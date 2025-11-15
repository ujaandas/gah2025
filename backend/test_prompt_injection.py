"""
Test file for the PromptInjectionNode.

This script creates a simple LangGraph workflow with a prompt injection node
and logs the before/after states to demonstrate the injection in action.
"""

import json
from langgraph.graph import StateGraph, START, END
from testing_nodes.prompt_injection_node import create_prompt_injection_node


def setup_test_graph():
    """Set up a simple graph with prompt injection for testing."""
    
    # Create a state graph
    graph = StateGraph(dict)
    
    # Step 1: Generate an initial prompt
    def generate_initial_prompt(state):
        """Generate a simple, benign prompt."""
        prompt = "What is the capital of France?"
        print("\n" + "="*80)
        print("STEP 1: GENERATING INITIAL PROMPT")
        print("="*80)
        print(f"Generated prompt: {prompt}")
        print(f"Full state: {json.dumps({'prompt': prompt}, indent=2)}")
        return {"prompt": prompt}
    
    # Step 2: Inject the prompt (using our testing node)
    injection_node = create_prompt_injection_node(
        node_id="injection_test",
        name="prompt_injection_test",
        ollama_model="llama2",
        ollama_base_url="http://localhost:11434",
        state_prompt_key="prompt",
        state_output_key="injected_prompt"
    )
    
    # Wrap the injection node to add logging
    def logged_injection(state):
        """Wrapper to log before and after injection."""
        print("\n" + "="*80)
        print("STEP 2: PROMPT INJECTION (BEFORE)")
        print("="*80)
        print(f"Original prompt: {state.get('prompt', 'N/A')}")
        print(f"State before injection: {json.dumps({k: v for k, v in state.items() if k != 'execution_history'}, indent=2)}")
        
        # Call the actual injection node
        print("\n" + "-"*80)
        print("Calling Ollama to inject the prompt...")
        print("-"*80)
        result = injection_node.data(state)
        
        print("\n" + "="*80)
        print("STEP 2: PROMPT INJECTION (AFTER)")
        print("="*80)
        print(f"Injected prompt: {result.get('injected_prompt', 'N/A')}")
        print(f"Injection applied: {result.get('injection_applied', 'N/A')}")
        if 'injection_error' in result:
            print(f"Injection error: {result['injection_error']}")
        
        # Show comparison
        print("\n" + "-"*80)
        print("COMPARISON:")
        print("-"*80)
        print(f"BEFORE:  {state.get('prompt', 'N/A')}")
        print(f"AFTER:   {result.get('injected_prompt', 'N/A')}")
        print("-"*80)
        
        return result
    
    # Step 3: Process the injected prompt (simulated LLM call)
    def process_prompt(state):
        """Simulate processing the potentially injected prompt."""
        print("\n" + "="*80)
        print("STEP 3: PROCESSING INJECTED PROMPT")
        print("="*80)
        
        # In a real scenario, this would be the actual LLM that might be vulnerable
        prompt_to_process = state.get("injected_prompt", state.get("prompt"))
        print(f"Processing prompt: {prompt_to_process}")
        
        # Simulated response
        response = f"[Simulated LLM Response] I received: {prompt_to_process[:100]}..."
        print(f"Simulated response: {response}")
        
        # Preserve all state including injection results
        return {
            **state,  # Preserve all previous state
            "final_response": response,
            "completed": True
        }
    
    # Build the graph
    graph.add_node("generate", generate_initial_prompt)
    graph.add_node("inject", logged_injection)
    graph.add_node("process", process_prompt)
    
    # Connect the nodes in sequence
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "inject")
    graph.add_edge("inject", "process")
    graph.add_edge("process", END)
    
    return graph.compile()


def run_test():
    """Run the test workflow."""
    print("\n" + "#"*80)
    print("# PROMPT INJECTION NODE TEST")
    print("#"*80)
    print("\nThis test demonstrates how the PromptInjectionNode transforms")
    print("a benign prompt into an adversarial one using Ollama.")
    print("\nStarting workflow...\n")
    
    try:
        # Set up and compile the graph
        workflow = setup_test_graph()
        
        # Run the workflow
        print("\n" + "="*80)
        print("EXECUTING WORKFLOW")
        print("="*80)
        
        result = workflow.invoke({})
        
        # Display final results
        print("\n" + "="*80)
        print("FINAL RESULTS")
        print("="*80)
        print(json.dumps({
            "completed": result.get("completed"),
            "original_prompt": result.get("original_prompt"),
            "injected_prompt": result.get("injected_prompt")[:200] + "..." if len(result.get("injected_prompt", "")) > 200 else result.get("injected_prompt"),
            "injection_applied": result.get("injection_applied"),
            "final_response": result.get("final_response")[:200] + "..." if len(result.get("final_response", "")) > 200 else result.get("final_response")
        }, indent=2))
        
        print("\n" + "#"*80)
        print("# TEST COMPLETED SUCCESSFULLY")
        print("#"*80)
        
        return result
        
    except Exception as e:
        print("\n" + "!"*80)
        print("! ERROR DURING TEST")
        print("!"*80)
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        
        print("\n" + "!"*80)
        print("! TEST FAILED")
        print("!"*80)
        
        raise


def run_multiple_tests():
    """Run multiple test cases with different prompts."""
    test_prompts = [
        "What is the capital of France?",
        "Tell me a joke",
        "How do I reset my password?",
    ]
    
    print("\n" + "#"*80)
    print("# RUNNING MULTIPLE TEST CASES")
    print("#"*80)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n\nTest Case {i}/{len(test_prompts)}: '{prompt}'")
        print("-"*80)
        
        try:
            # Create a custom graph for this test
            graph = StateGraph(dict)
            
            def make_prompt_generator(p):
                def generate_prompt(state):
                    print(f"\nOriginal: {p}")
                    return {"prompt": p}
                return generate_prompt
            
            injection_node = create_prompt_injection_node(
                node_id=f"injection_test_{i}",
                ollama_model="llama2"
            )
            
            def inject_and_log(state):
                result = injection_node.data(state)
                print(f"Injected: {result.get('injected_prompt', 'ERROR')[:150]}...")
                return result
            
            graph.add_node("gen", make_prompt_generator(prompt))
            graph.add_node("inject", inject_and_log)
            
            graph.add_edge(START, "gen")
            graph.add_edge("gen", "inject")
            graph.add_edge("inject", END)
            
            workflow = graph.compile()
            result = workflow.invoke({})
            
            print(f"✓ Test {i} completed")
            
        except Exception as e:
            print(f"✗ Test {i} failed: {str(e)}")


if __name__ == "__main__":
    import sys
    
    # Check if Ollama is running
    print("Checking if Ollama is available...")
    try:
        import httpx
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:11434/api/version")
            response.raise_for_status()
            print(f"✓ Ollama is running (version: {response.json().get('version')})")
    except Exception as e:
        print(f"✗ Error: Ollama is not running or not accessible")
        print(f"  {str(e)}")
        print("\nPlease start Ollama with: ollama serve")
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--multiple":
        run_multiple_tests()
    else:
        run_test()

