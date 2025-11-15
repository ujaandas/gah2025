#!/usr/bin/env python3
"""
Quick demo of the Fuzzer Node

Run this for a quick demonstration of fuzzer capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from testing_nodes.fuzzer_node import PromptFuzzer


def main():
    print("\n" + "🎯" * 30)
    print("FUZZER NODE DEMO")
    print("🎯" * 30)
    
    print("\n📝 This demo will:")
    print("   1. Connect to your local Ollama instance (llama3.2:latest - faster!)")
    print("   2. Take a simple prompt and generate 15 adversarial variants")
    print("   3. Test each variant and show results")
    print("   4. Generate an analysis report")
    
    input("\n👉 Press Enter to start (or Ctrl+C to cancel)...")
    
    # Initialize fuzzer
    print("\n🔌 Connecting to Ollama...")
    fuzzer = PromptFuzzer(model="llama3.2:latest")
    
    # Test connection
    if not fuzzer.test_ollama_connection():
        print("\n❌ Cannot proceed without Ollama connection.")
        print("\n💡 Setup:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Pull model: ollama pull llama3.2:latest")
        print("   3. Run demo again: python demo_fuzzer.py")
        sys.exit(1)
    
    print("✅ Connected successfully!")
    
    # Get prompt from user
    print("\n" + "─" * 60)
    default_prompt = "Explain quantum computing in simple terms"
    user_prompt = input(f"Enter a prompt to test (or press Enter for default):\n> ")
    
    if not user_prompt.strip():
        user_prompt = default_prompt
        print(f"Using default: {user_prompt}")
    
    # Show what variants will be generated
    print("\n📊 Generating variant types:")
    print("   ✓ Instruction overrides (prompt injection attempts)")
    print("   ✓ Malformed inputs (edge cases)")
    print("   ✓ Adversarial prompts (contradictions)")
    print("   ✓ Boundary tests (extreme values)")
    print("   ✓ Noise variants (typos, corruption)")
    
    input("\n👉 Press Enter to start fuzzing...")
    
    # Run fuzzing
    print("\n" + "─" * 60)
    results = fuzzer.fuzz_prompt(
        prompt=user_prompt,
        max_variants=15,
        include_overrides=True,
        include_malformed=True,
        include_adversarial=True,
        include_boundary=True,
        include_noise=True
    )
    
    # Show some interesting results
    print("\n" + "─" * 60)
    print("🔍 INTERESTING FINDINGS")
    print("─" * 60)
    
    # Group results by type
    by_type = {}
    for result in results:
        if result.variant_type not in by_type:
            by_type[result.variant_type] = []
        by_type[result.variant_type].append(result)
    
    # Show one example from each type
    for variant_type, type_results in by_type.items():
        successful = [r for r in type_results if r.success]
        if successful:
            example = successful[0]
            print(f"\n📌 {variant_type.upper()}")
            print(f"   Fuzzed: {example.fuzzed_prompt[:100]}...")
            print(f"   Response: {example.response[:150]}...")
            print(f"   Time: {example.response_time_ms:.0f}ms | Tokens: {example.tokens_used}")
    
    # Generate and print full report
    fuzzer.print_report()
    
    # Show recommendations
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATIONS")
    print("=" * 60)
    
    report = fuzzer.analyze_results()
    success_rate = report['summary']['success_rate']
    
    if success_rate < 70:
        print("⚠️  Low success rate detected!")
        print("   - Model may be refusing many prompts")
        print("   - Consider reviewing refusal patterns")
    elif success_rate > 95:
        print("✅ High success rate - model handles most variants")
        print("   - Check if any adversarial prompts succeeded unexpectedly")
        print("   - Review anomalies for potential vulnerabilities")
    else:
        print("✅ Moderate success rate - normal behavior")
        print("   - Model shows some resistance to adversarial inputs")
    
    if report['anomalies']['count'] > 0:
        print(f"\n⚠️  {report['anomalies']['count']} anomalies detected")
        print("   - These responses differ significantly from average")
        print("   - Review them for potential issues")
    
    print("\n" + "=" * 60)
    print("✨ Demo complete! Check the detailed report above.")
    print("=" * 60)
    
    # Offer to run again
    print("\n👉 Want to test another prompt?")
    print("   Run: python demo_fuzzer.py")
    print("\n👉 Want to run full tests?")
    print("   Run: python test_fuzzer.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

