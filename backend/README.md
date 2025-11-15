# Fuzzer Node Testing

This directory contains the Fuzzer Node implementation and tests for adversarial prompt testing.

## Quick Start

### 1. Setup Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
# In a separate terminal
ollama serve

# Your Ollama is already running with llama3.2:latest model
```

### 3. Run Tests

#### Quick Test (Fastest - Automated)
```bash
python quick_test_fuzzer.py
```

This runs a simple LangGraph workflow with the fuzzer node, showing:
- Clear **before/after** logging (input → model → output)
- 5 test variants
- Results saved to `fuzzer_logs/quick_test.json`

#### Full Test Suite
```bash
# Run all 7 tests
python testing_nodes/test_fuzzer.py

# Run specific test
python testing_nodes/test_fuzzer.py --test 3

# Quick tests only (no LLM calls)
python testing_nodes/test_fuzzer.py --quick
```

#### LangGraph Integration Test (Interactive)
```bash
python test_fuzzer_graph.py
```

Shows detailed LangGraph integration with multiple output formats.

## What is the Fuzzer Node?

The Fuzzer Node is a **testing node** that:
1. Takes your prompt
2. Generates adversarial variants (50+ types):
   - Instruction overrides (prompt injection attacks)
   - Malformed inputs (edge cases)
   - Adversarial prompts (contradictions)
   - Boundary tests (extreme values)
   - Noise variants (typos, corruption)
3. Tests each variant against your LLM
4. Logs all responses
5. Analyzes patterns and anomalies

## Output Formats

The fuzzer supports 3 output formats:

### JSON (Best for programmatic access)
```python
"fuzzer_config": {
    "output_file": "results.json",
    "output_format": "json"
}
```

### CSV (Best for Excel/spreadsheet analysis)
```python
"fuzzer_config": {
    "output_file": "results.csv",
    "output_format": "csv"
}
```

### Text (Best for human reading)
```python
"fuzzer_config": {
    "output_file": "results.txt",
    "output_format": "text"
}
```

## Usage in LangGraph

```python
from langgraph.graph import StateGraph, START, END
from testing_nodes.fuzzer_node import fuzzer_node_function

# Define state
class MyState(TypedDict):
    prompt: str
    fuzzer_config: dict
    fuzzer_results: list
    fuzzer_report: dict

# Build graph
graph = StateGraph(MyState)
graph.add_node("fuzzer", fuzzer_node_function)
graph.add_edge(START, "fuzzer")
graph.add_edge("fuzzer", END)
compiled = graph.compile()

# Run
state = {
    "prompt": "Your prompt here",
    "fuzzer_config": {
        "model": "llama3.2:latest",
        "max_variants": 10,
        "output_file": "fuzzer_logs/results.json",
    }
}

result = compiled.invoke(state)
```

## Configuration Options

```python
"fuzzer_config": {
    # Model settings
    "model": "llama3.2:latest",           # Ollama model to use
    "max_variants": 20,                    # Max variants to test
    
    # Variant types (all default to True)
    "include_overrides": True,             # Instruction override attacks
    "include_malformed": True,             # Malformed/edge case inputs
    "include_adversarial": True,           # Adversarial prompts
    "include_boundary": True,              # Boundary/extreme values
    "include_noise": True,                 # Noisy variants
    
    # Output settings
    "output_file": "results.json",         # Where to save results
    "output_format": "json",               # json, csv, or text
    "append_results": False,               # Append to existing file
}
```

## Output Structure

### Results
Each test includes:
- `variant_type`: Type of fuzzing applied
- `original_prompt`: Your original prompt
- `fuzzed_prompt`: The variant tested
- `response`: Model's response
- `success`: Whether test completed
- `tokens_used`: Number of tokens generated
- `response_time_ms`: Response time in milliseconds
- `timestamp`: When test ran

### Analysis Report
Includes:
- **Summary**: Total tests, success rate
- **By Variant Type**: Breakdown per type
- **Performance**: Avg response time, tokens
- **Anomalies**: Unusual responses flagged

## Files

- `quick_test_fuzzer.py` - Quick automated test (recommended)
- `test_fuzzer_graph.py` - Full LangGraph integration demo (interactive)
- `testing_nodes/fuzzer_node.py` - Main fuzzer implementation
- `testing_nodes/test_fuzzer.py` - Unit tests
- `testing_nodes/test_logging.py` - Logging tests
- `fuzzer_logs/` - Output directory for results

## Model Selection

**Current Default:** `llama3.2:latest` (2GB, fast)

Other options:
- `gemma3:4b` (3.3GB, more capable but slower)
- Any other Ollama model

Change in config:
```python
"fuzzer_config": {"model": "your-model-name"}
```

## Tips

1. **Start small**: Use `max_variants: 5` for quick tests
2. **Use JSON format**: Best for post-processing and analysis
3. **Enable append mode**: Track results across multiple runs
4. **Check anomalies**: Flag unusual behaviors
5. **Test critical prompts**: Use fuzzer on production-bound prompts

## Troubleshooting

### "Could not connect to Ollama"
```bash
# Start Ollama server
ollama serve

# Verify model is available
ollama list
```

### "Module not found: langgraph"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Tests are slow
- Reduce `max_variants` to 5-10
- Use `llama3.2:latest` (faster model)
- Check system resources

## Next Steps

1. Run `python quick_test_fuzzer.py` to verify setup
2. Check output in `fuzzer_logs/quick_test.json`
3. Integrate fuzzer node into your LangGraph workflow
4. Test your critical prompts for vulnerabilities

