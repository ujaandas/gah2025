"""
Quick test script for the FuzzerNode.

This is a simple script to quickly verify the fuzzer is working.
"""

import logging
from testing_nodes.fuzzer_node import create_fuzzer_node

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def quick_test():
    """Run a quick test of the fuzzer."""
    logger.info("\n" + "="*70)
    logger.info("QUICK FUZZER TEST")
    logger.info("="*70 + "\n")
    
    # Create a simple fuzzer
    logger.info("Creating fuzzer node...")
    fuzzer = create_fuzzer_node(
        node_id="quick_test",
        name="quick_test_fuzzer",
        fuzzing_strategies=["prompt_injection", "sql_injection", "xss_injection"],
        mutation_rate=1.0,
        save_logs=True,
        log_file="fuzzer_logs/quick_test.json"
    )
    
    # Test input
    test_state = {
        "prompt": "What is the meaning of life?"
    }
    
    logger.info(f"\nTest input: {test_state}\n")
    
    # Run fuzzer
    logger.info("Running fuzzer...\n")
    result = fuzzer.data(test_state)
    
    # Display results
    logger.info("\n" + "="*70)
    logger.info("RESULTS")
    logger.info("="*70)
    print(f"\n📝 Original prompt: {test_state['prompt']}")
    print(f"\n🔥 Fuzzed prompt: {result['fuzzed_prompt']}")
    print(f"\n🎯 Strategy used: {result['fuzzed_prompt_strategy']}")
    print(f"\n💾 Log saved to: fuzzer_logs/quick_test.json\n")
    
    logger.info("="*70)
    logger.info("TEST COMPLETE")
    logger.info("="*70)
    
    return result


if __name__ == "__main__":
    print("\n🚀 Quick Fuzzer Test")
    print("="*70)
    print("Testing fuzzer with multiple attack strategies...")
    print("="*70 + "\n")
    
    try:
        result = quick_test()
        print("\n✅ Test completed successfully!")
        print("\n📋 Check fuzzer_logs/quick_test.json for detailed results")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
