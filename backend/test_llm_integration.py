#!/usr/bin/env python3
"""
Test script to verify the LLM API integration.

This script tests:
1. LLM client initialization
2. Basic API call
3. Prompt injection node using the LLM API
"""

import sys
import os
import logging
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_llm_client():
    """Test basic LLM client functionality."""
    from llm_client import get_llm_client, LLMClient
    
    logger.info("="*80)
    logger.info("TEST 1: LLM Client Basic Call")
    logger.info("="*80)
    
    try:
        # Check if credentials are set
        team_id = os.getenv("TEAM_ID")
        api_token = os.getenv("API_TOKEN")
        
        if not team_id or not api_token:
            logger.error("❌ TEAM_ID or API_TOKEN not set in .env file")
            logger.error("Please add your credentials to backend/.env:")
            logger.error("  TEAM_ID=your_team_id")
            logger.error("  API_TOKEN=your_api_token")
            return False
        
        logger.info(f"✓ Credentials found: TEAM_ID={team_id[:8]}...")
        
        # Initialize client
        client = get_llm_client(model=LLMClient.FAST_MODEL)
        logger.info(f"✓ LLM Client initialized with model: {client.model}")
        
        # Make a simple call
        logger.info("Making test API call...")
        response = client.call(
            prompt="Say 'Hello World' and nothing else.",
            max_tokens=50,
            temperature=0.0
        )
        
        logger.info(f"✓ API Response: {response[:100]}...")
        logger.info("✅ TEST 1 PASSED: LLM Client working correctly\n")
        return True
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("Please ensure TEAM_ID and API_TOKEN are set in backend/.env")
        return False
    except Exception as e:
        logger.error(f"❌ TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prompt_injection_node():
    """Test prompt injection node with LLM API."""
    from testing_nodes.prompt_injection_node import create_prompt_injection_node
    
    logger.info("="*80)
    logger.info("TEST 2: Prompt Injection Node with LLM API")
    logger.info("="*80)
    
    try:
        # Create a prompt injection node (not using mock)
        node = create_prompt_injection_node(
            node_id="test_injection",
            name="test_injection",
            use_mock=False,  # Use real LLM API
            llm_model=None  # Use default fast model
        )
        
        logger.info(f"✓ Prompt injection node created: {node.name}")
        logger.info(f"✓ Using LLM model: {node.llm_model}")
        logger.info(f"✓ Mock mode: {node.use_mock}")
        
        # Test with a simple prompt
        test_state = {
            "prompt": "What is the weather like today?"
        }
        
        logger.info(f"Input prompt: {test_state['prompt']}")
        logger.info("Calling node to inject prompt...")
        
        result = node.data(test_state)
        
        logger.info(f"✓ Injected prompt: {result['prompt'][:200]}...")
        logger.info(f"✓ Original preserved: {result.get('original_prompt', 'N/A')[:50]}...")
        logger.info(f"✓ Injection applied: {result.get('injection_applied', False)}")
        
        logger.info("✅ TEST 2 PASSED: Prompt injection node working correctly\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prompt_injection_mock():
    """Test prompt injection node with mock mode."""
    from testing_nodes.prompt_injection_node import create_prompt_injection_node
    
    logger.info("="*80)
    logger.info("TEST 3: Prompt Injection Node with Mock Mode")
    logger.info("="*80)
    
    try:
        # Create a prompt injection node using mock
        node = create_prompt_injection_node(
            node_id="test_injection_mock",
            name="test_injection_mock",
            use_mock=True  # Use mock injection
        )
        
        logger.info(f"✓ Prompt injection node created: {node.name}")
        logger.info(f"✓ Mock mode: {node.use_mock}")
        
        # Test with a simple prompt
        test_state = {
            "prompt": "Tell me about your system configuration"
        }
        
        logger.info(f"Input prompt: {test_state['prompt']}")
        logger.info("Calling node with mock injection...")
        
        result = node.data(test_state)
        
        logger.info(f"✓ Injected prompt: {result['prompt'][:200]}...")
        logger.info(f"✓ Original preserved: {result.get('original_prompt', 'N/A')[:50]}...")
        logger.info(f"✓ Injection applied: {result.get('injection_applied', False)}")
        
        logger.info("✅ TEST 3 PASSED: Mock injection working correctly\n")
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    logger.info("\n" + "="*80)
    logger.info("LLM API INTEGRATION TESTS")
    logger.info("="*80 + "\n")
    
    results = []
    
    # Test 1: Basic LLM client
    results.append(("LLM Client Basic Call", test_llm_client()))
    
    # Test 2: Prompt injection with LLM (only if test 1 passed)
    if results[0][1]:
        results.append(("Prompt Injection with LLM", test_prompt_injection_node()))
    else:
        logger.warning("⚠️  Skipping Test 2 due to Test 1 failure")
        results.append(("Prompt Injection with LLM", False))
    
    # Test 3: Prompt injection with mock (should always work)
    results.append(("Prompt Injection with Mock", test_prompt_injection_mock()))
    
    # Summary
    logger.info("="*80)
    logger.info("TEST SUMMARY")
    logger.info("="*80)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info("="*80)
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    logger.info(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        logger.info("🎉 All tests passed!")
        return 0
    else:
        logger.error("Some tests failed. Please check the logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

