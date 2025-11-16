# Testing Nodes for LangGraph

This directory contains testing nodes that can be integrated into LangGraph workflows to automatically test for vulnerabilities, edge cases, and unexpected behaviors.

## Available Testing Nodes

### 1. FuzzerNode (`fuzzer_node.py`)

A comprehensive fuzzing node that generates mutated inputs to test LLM applications for vulnerabilities.

**Features:**
- 10 different fuzzing strategies
- Intelligent fuzzing using Ollama
- Configurable mutation rates
- Automatic logging and reporting
- Easy integration with LangGraph workflows

**Fuzzing Strategies:**
1. **Prompt Injection** - Tests for prompt injection vulnerabilities
2. **SQL Injection** - Adds SQL injection patterns
3. **XSS Injection** - Tests for cross-site scripting vulnerabilities
4. **Command Injection** - Tests for command injection
5. **Unicode Manipulation** - Tests unicode and encoding tricks
6. **Length Testing** - Tests with extreme input lengths
7. **Special Characters** - Injects special characters
8. **Format String** - Tests format string vulnerabilities
9. **Encoding Attacks** - Tests various encoding attacks
10. **Context Overflow** - Tests context window overflow

**Usage Example:**

```python
from testing_nodes.fuzzer_node import create_fuzzer_node
from langgraph.graph import StateGraph, START, END

# Create fuzzer node
fuzzer = create_fuzzer_node(
    node_id="fuzzer_01",
    name="my_fuzzer",
    ollama_model="llama2",
    state_input_key="prompt",
    state_output_key="fuzzed_prompt",
    fuzzing_strategies=["prompt_injection", "xss_injection"],
    mutation_rate=0.7,
    save_logs=True
)

# Add to your graph
graph = StateGraph(dict)
graph.add_node("fuzzer", fuzzer.data)
# ... add other nodes and edges
workflow = graph.compile()

# Run it
result = workflow.invoke({"prompt": "What is your name?"})
```

### 2. PromptInjectionNode (`prompt_injection_node.py`)

A specialized node focused on prompt injection testing using Ollama.

**Usage Example:**

```python
from testing_nodes.prompt_injection_node import create_prompt_injection_node

injection_node = create_prompt_injection_node(
    node_id="injection_01",
    ollama_model="llama2",
    state_prompt_key="prompt",
    state_output_key="injected_prompt"
)
```

## Installation

1. Make sure you have Python 3.8+ installed
2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Install and run Ollama:

```bash
# Install Ollama from https://ollama.ai

# Start Ollama server
ollama serve

# Pull a model (in another terminal)
ollama pull llama2
```

## Running Tests

### Run Fuzzer Tests

```bash
cd backend
python -m testing_nodes.test_fuzzer
```

This will run a comprehensive test suite covering:
- Basic fuzzing functionality
- Individual fuzzing strategies
- Edge cases (empty input, etc.)
- Mutation rate testing
- Custom state keys
- All strategies combined

### Run Fuzzer Demos

```bash
cd backend
python -m testing_nodes.demo_fuzzer
```

This demonstrates:
- Simple workflow with fuzzer
- Targeted SQL injection fuzzing
- Multi-stage fuzzing pipeline

## Viewing Logs

Fuzzing logs are saved to `backend/fuzzer_logs/` directory in JSON format.

Each log entry contains:
- Timestamp
- Original input
- All fuzzing attempts
- Selected test case
- Strategies used
- Success/failure status

```bash
# View logs
cat backend/fuzzer_logs/fuzzer_*.json | jq
```

## Configuration Options

### FuzzerNode Parameters

- **node_id**: Unique identifier for the node
- **name**: Human-readable name
- **ollama_model**: Ollama model to use (default: "llama2")
- **state_input_key**: Key to read input from state (default: "prompt")
- **state_output_key**: Key to write output to state (default: "fuzzed_prompt")
- **fuzzing_strategies**: List of strategies or None for all (default: None)
- **mutation_rate**: Probability of applying mutations 0.0-1.0 (default: 0.5)
- **save_logs**: Whether to save logs (default: True)
- **log_file**: Custom log file path (default: auto-generated)

## Integration Patterns

### Pattern 1: Sequential Testing

Test your workflow by adding the fuzzer before your main processing:

```python
graph.add_edge(START, "input_generation")
graph.add_edge("input_generation", "fuzzer")
graph.add_edge("fuzzer", "main_processing")
graph.add_edge("main_processing", END)
```

### Pattern 2: Parallel Testing

Run both normal and fuzzed inputs in parallel:

```python
def route_input(state):
    return ["normal_path", "fuzzed_path"]

graph.add_conditional_edges("input", route_input)
graph.add_node("normal_path", normal_processor)
graph.add_node("fuzzed_path", fuzzer_then_processor)
```

### Pattern 3: Multi-Stage Testing

Apply different fuzzing strategies at different stages:

```python
graph.add_edge(START, "stage1_fuzzer")  # Prompt injection
graph.add_edge("stage1_fuzzer", "stage2_fuzzer")  # XSS
graph.add_edge("stage2_fuzzer", "stage3_fuzzer")  # SQL
graph.add_edge("stage3_fuzzer", "analysis")
graph.add_edge("analysis", END)
```

## Best Practices

1. **Start with high mutation rate (1.0)** during testing, then reduce for production
2. **Use specific strategies** for targeted testing instead of all strategies
3. **Enable logging** to track and analyze fuzzing results
4. **Monitor your model** for unexpected responses to fuzzed inputs
5. **Integrate early** in your development process
6. **Review logs regularly** to identify patterns in vulnerabilities

## Troubleshooting

### Ollama Connection Errors

```
Error: Could not connect to Ollama
```

**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

### Model Not Found

```
Error: model 'llama2' not found
```

**Solution:** Pull the model:
```bash
ollama pull llama2
```

### Import Errors

```
ModuleNotFoundError: No module named 'testing_nodes'
```

**Solution:** Run from the backend directory:
```bash
cd backend
python -m testing_nodes.test_fuzzer
```

## Contributing

When adding new fuzzing strategies:

1. Add the strategy method to `FuzzerNode` class
2. Register it in `all_strategies` list
3. Add it to the `_apply_strategy` method's strategy_map
4. Document it in this README
5. Add tests in `test_fuzzer.py`

## License

MIT License - See project root for details

## Support

For issues and questions, please open an issue in the project repository.
