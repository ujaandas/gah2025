# LLM API Migration Guide

This document describes the migration from Ollama to the team's LLM API endpoint.

## What Changed

### Before (Ollama)
- Used local Ollama server at `http://localhost:11434`
- Required local model installation
- Model: `dolphin-phi` or similar local models

### After (Team LLM API)
- Uses cloud-based LLM API: `https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke`
- No local setup required
- Supports multiple models from Anthropic, Meta, Amazon Nova, Mistral, and DeepSeek

## Setup

### 1. Environment Variables

Create or update `/backend/.env` with your team credentials:

```bash
TEAM_ID=your_team_id
API_TOKEN=your_api_token
```

**Important:** Never commit the `.env` file to git. It's already in `.gitignore`.

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The new dependencies include:
- `python-dotenv` - For loading environment variables
- `httpx` - For HTTP requests (already present)

Removed dependencies:
- `ollama` - No longer needed

### 3. Test the Integration

Run the test script to verify everything works:

```bash
cd backend
python test_llm_integration.py
```

This will test:
1. LLM client initialization
2. Basic API calls
3. Prompt injection node with LLM API
4. Mock mode (as fallback)

## Available Models

### Recommended Models

- **Default Model:** `us.anthropic.claude-3-5-sonnet-20241022-v2:0` (Balanced)
- **Fast Model:** `us.anthropic.claude-3-5-haiku-20241022-v1:0` (Quick responses)
- **Powerful Model:** `us.anthropic.claude-3-opus-20240229-v1:0` (Best quality)

### All Available Models

**Anthropic Claude:**
- `us.anthropic.claude-3-5-sonnet-20241022-v2:0` ⭐ Recommended
- `us.anthropic.claude-3-5-haiku-20241022-v1:0` ⚡ Fast
- `us.anthropic.claude-3-opus-20240229-v1:0` 💪 Most Powerful
- `us.anthropic.claude-3-sonnet-20240229-v1:0`
- `us.anthropic.claude-3-haiku-20240307-v1:0`
- `us.anthropic.claude-opus-4-20250514-v1:0`
- `us.anthropic.claude-sonnet-4-20250514-v1:0`
- `us.anthropic.claude-sonnet-4-5-20250929-v1:0`
- `us.anthropic.claude-haiku-4-5-20251001-v1:0`

**Meta Llama:**
- `us.meta.llama3-2-90b-instruct-v1:0` Large
- `us.meta.llama3-2-11b-instruct-v1:0` Balanced
- `us.meta.llama3-2-3b-instruct-v1:0` Lightweight
- `us.meta.llama3-2-1b-instruct-v1:0` Ultra-light
- `us.meta.llama3-1-70b-instruct-v1:0`
- `us.meta.llama3-1-8b-instruct-v1:0`
- `us.meta.llama3-3-70b-instruct-v1:0`
- `us.meta.llama4-scout-17b-instruct-v1:0`
- `us.meta.llama4-maverick-17b-instruct-v1:0`

**Amazon Nova:**
- `us.amazon.nova-premier-v1:0` Most Powerful
- `us.amazon.nova-pro-v1:0` ⭐ Recommended
- `us.amazon.nova-lite-v1:0` Fast
- `us.amazon.nova-micro-v1:0` Ultra-fast

**Mistral:**
- `us.mistral.pixtral-large-2502-v1:0` Large
- `mistral.mistral-large-2402-v1:0`
- `mistral.mistral-small-2402-v1:0` Fast
- `mistral.mistral-7b-instruct-v0:2`
- `mistral.mixtral-8x7b-instruct-v0:1`

**DeepSeek:**
- `us.deepseek.r1-v1:0` Latest

## Usage

### Using the LLM Client Directly

```python
from llm_client import get_llm_client, LLMClient

# Get client instance (uses env vars for credentials)
client = get_llm_client()

# Make a simple call
response = client.call(
    prompt="What is prompt injection?",
    max_tokens=512,
    temperature=0.7
)
print(response)

# Use a specific model
client_fast = get_llm_client(model=LLMClient.FAST_MODEL)
response = client_fast.call(prompt="Quick question: What is 2+2?")
```

### Using Prompt Injection Node

```python
from testing_nodes.prompt_injection_node import create_prompt_injection_node

# Create node with LLM API (default)
node = create_prompt_injection_node(
    node_id="injection_1",
    name="prompt_injection",
    use_mock=False,  # Use real LLM API
    llm_model=None  # Uses default fast model
)

# Use with a custom model
node = create_prompt_injection_node(
    node_id="injection_2",
    llm_model="us.anthropic.claude-3-opus-20240229-v1:0"  # More powerful
)

# Use mock mode (no API calls, faster for testing)
node_mock = create_prompt_injection_node(
    node_id="injection_mock",
    use_mock=True
)
```

### Via API Service

When using the API, the configuration has changed:

**Old Configuration (Ollama):**
```json
{
  "use_mock": false,
  "ollama_base_url": "http://localhost:11434",
  "ollama_model": "dolphin-phi"
}
```

**New Configuration (LLM API):**
```json
{
  "use_mock": false,
  "llm_model": null  // or specify a model like "us.anthropic.claude-3-5-haiku-20241022-v1:0"
}
```

## Code Changes Summary

### New Files
- `backend/llm_client.py` - Centralized LLM API client
- `backend/test_llm_integration.py` - Integration tests
- `backend/LLM_API_MIGRATION.md` - This file

### Modified Files
- `backend/testing_nodes/prompt_injection_node.py` - Updated to use LLM API
- `api/services/testing_service.py` - Updated configuration
- `backend/requirements.txt` - Added `python-dotenv`, removed `ollama`
- `api/requirements.txt` - Added `python-dotenv`

### Removed Dependencies
- `ollama` package

## API Features

### Basic Call
```python
response = client.call(
    prompt="Your prompt here",
    system_prompt="Optional system prompt",
    max_tokens=1024,
    temperature=0.7
)
```

### Multi-turn Conversation
```python
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "Tell me about AI"}
]

response = client.call_with_messages(
    messages=messages,
    max_tokens=1024
)
```

### Tool Calling (Claude, DeepSeek, Amazon Nova)
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

result = client.call_with_tools(
    prompt="What's the weather in San Francisco?",
    tools=tools,
    tool_choice="auto"
)
```

## Error Handling

The LLM client includes automatic fallback to mock mode if API calls fail:

```python
# If the LLM API fails, prompt injection nodes automatically fall back to mock mode
try:
    injected = node.data({"prompt": "test"})
except Exception as e:
    # Node will log the error and use mock injection instead
    pass
```

## Testing

### Run All Tests
```bash
cd backend
python test_llm_integration.py
```

### Expected Output
```
TEST 1: LLM Client Basic Call
✓ Credentials found
✓ LLM Client initialized
✓ API Response received
✅ TEST 1 PASSED

TEST 2: Prompt Injection with LLM
✓ Node created
✓ Injection successful
✅ TEST 2 PASSED

TEST 3: Prompt Injection with Mock
✓ Node created
✓ Mock injection successful
✅ TEST 3 PASSED

Total: 3/3 tests passed
🎉 All tests passed!
```

## Troubleshooting

### Issue: "TEAM_ID must be provided or set in environment variables"
**Solution:** Create `backend/.env` with your credentials:
```bash
TEAM_ID=your_team_id
API_TOKEN=your_api_token
```

### Issue: "HTTP error calling LLM API"
**Solution:** 
1. Check your credentials are correct
2. Verify your team has API access
3. Check network connectivity
4. The node will automatically fall back to mock mode

### Issue: "Unexpected response format"
**Solution:** This usually means the model returned a different format. The client will try to extract text from various formats. If this persists, use a different model.

## Performance

### Model Selection Guidelines

- **Fast responses needed:** Use `us.anthropic.claude-3-5-haiku-20241022-v1:0`
- **Balanced quality/speed:** Use `us.anthropic.claude-3-5-sonnet-20241022-v2:0` (default)
- **Best quality:** Use `us.anthropic.claude-3-opus-20240229-v1:0`
- **Cost-effective:** Use `us.amazon.nova-micro-v1:0` or `us.meta.llama3-2-1b-instruct-v1:0`

### Timeout Settings

Default timeout is 120 seconds. Adjust if needed:

```python
client = LLMClient(timeout=180.0)  # 3 minutes
```

## Migration Checklist

- [x] Install `python-dotenv`
- [x] Remove `ollama` dependency
- [x] Create `.env` file with credentials
- [x] Update `prompt_injection_node.py`
- [x] Update `testing_service.py`
- [x] Create `llm_client.py`
- [x] Create test script
- [ ] Test with your credentials
- [ ] Update any custom nodes using Ollama

## Support

If you encounter issues:

1. Check the test script: `python test_llm_integration.py`
2. Verify credentials in `.env`
3. Check logs for detailed error messages
4. Try mock mode as a fallback: `use_mock=True`

## Notes

- The old Ollama parameters (`ollama_base_url`, `ollama_model`) are no longer used
- Mock mode still works and doesn't require API credentials
- All API calls are logged with detailed debug information
- The client automatically handles response cleaning and parsing

