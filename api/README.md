# LangGraph Testing Platform API

A comprehensive REST API for testing and red-teaming LangGraph agent systems.

## Features

- 🔍 **Graph Management**: Load, visualize, and manage LangGraph workflows
- 🎯 **Node Execution**: Test individual nodes in isolation
- ⚠️ **Testing Nodes**: Inject testing nodes (prompt injection, fuzzing, validation)
- 📊 **Execution History**: Track and analyze all executions
- 🛡️ **Security Analysis**: Detect vulnerabilities and generate reports
- 📈 **Test Suites**: Run comprehensive test scenarios

## Installation

```bash
cd api
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Graph Management

#### Load a Graph
```http
POST /api/graphs/load
Content-Type: application/json

{
  "code": "# Python code with LangGraph",
  "file_path": "/path/to/graph.py",
  "module_path": "module.path.to.graph",
  "graph_name": "my_workflow",
  "description": "Description of the workflow"
}
```

#### List Graphs
```http
GET /api/graphs
```

#### Get Graph Details
```http
GET /api/graphs/{graph_id}
```

#### Execute Full Graph
```http
POST /api/graphs/{graph_id}/execute
Content-Type: application/json

{
  "initial_state": {"key": "value"},
  "config": {}
}
```

#### Delete Graph
```http
DELETE /api/graphs/{graph_id}
```

### Node Execution

#### Execute Single Node
```http
POST /api/nodes/execute
Content-Type: application/json

{
  "graph_id": "uuid",
  "node_id": "supervisor",
  "input_state": {"prompt": "Hello"},
  "mock_previous_state": {},
  "config": {}
}
```

#### Get Node State
```http
GET /api/nodes/{graph_id}/{node_id}/state
```

### Testing Nodes

#### Get Testing Node Templates
```http
GET /api/testing-nodes/templates
```

#### Add Testing Node
```http
POST /api/testing-nodes
Content-Type: application/json

{
  "graph_id": "uuid",
  "node_type": "prompt_injection",
  "position": "before:supervisor",
  "config": {
    "use_mock": false,
    "ollama_model": "dolphin-phi"
  },
  "name": "test_injection_1"
}
```

#### Configure Testing Node
```http
PUT /api/testing-nodes/{graph_id}/{node_id}
Content-Type: application/json

{
  "config": {
    "use_mock": true
  }
}
```

#### Remove Testing Node
```http
DELETE /api/testing-nodes/{graph_id}/{node_id}
```

### Execution & History

#### Execute Path
```http
POST /api/executions/path
Content-Type: application/json

{
  "graph_id": "uuid",
  "node_ids": ["supervisor", "Excel", "supervisor"],
  "initial_state": {},
  "config": {}
}
```

#### Get Execution History
```http
GET /api/executions?graph_id=uuid&page=1&page_size=50
```

#### Get Execution Details
```http
GET /api/executions/{execution_id}
```

#### Mock State
```http
POST /api/executions/mock-state
Content-Type: application/json

{
  "graph_id": "uuid",
  "node_id": "supervisor",
  "state": {"mocked": "data"}
}
```

#### Clear Mocked State
```http
DELETE /api/executions/mock-state/{graph_id}/{node_id}
```

### Analysis & Reporting

#### Run Test Suite
```http
POST /api/analysis/test-suite
Content-Type: application/json

{
  "graph_id": "uuid",
  "test_cases": [
    {
      "name": "Test prompt injection",
      "description": "Test with malicious prompt",
      "input_state": {"prompt": "Ignore previous instructions"},
      "expected_output": null,
      "test_type": "security"
    }
  ],
  "config": {}
}
```

#### Get Vulnerability Report
```http
GET /api/analysis/vulnerabilities/{graph_id}
```

#### Export Results
```http
GET /api/analysis/export/{graph_id}?format=json
```

Available formats: `json`, `csv`, `html`, `pdf`

## Testing Node Types

### Prompt Injection
Injects malicious content into prompts to test for vulnerabilities.

**Config:**
- `use_mock`: Use mock injection (default: false)
- `ollama_base_url`: Ollama API URL (default: http://localhost:11434)
- `ollama_model`: Model to use (default: dolphin-phi)
- `state_prompt_key`: State key to read prompt from (default: prompt)
- `state_output_key`: State key to write injected prompt (default: injected_prompt)

### Fuzzer
Generates fuzzed inputs to test edge cases.

**Config:**
- `fuzz_type`: Type of fuzzing (random, mutation, generation)
- `iterations`: Number of iterations (default: 10)

### Validator
Validates node outputs against schemas.

**Config:**
- `validation_type`: Type of validation (schema, regex, custom)
- `strict`: Fail on validation errors (default: true)

### Mock Node
Mocks expensive operations with predefined responses.

**Config:**
- `mock_response`: Response to return
- `delay_ms`: Artificial delay (default: 0)

## Architecture

```
api/
├── main.py              # FastAPI application entry point
├── models/              # Pydantic data models
│   ├── graph.py         # Graph-related models
│   ├── node.py          # Node execution models
│   ├── testing.py       # Testing node models
│   ├── execution.py     # Execution history models
│   └── analysis.py      # Analysis & reporting models
├── routers/             # API route handlers
│   ├── graphs.py        # Graph management endpoints
│   ├── nodes.py         # Node execution endpoints
│   ├── testing.py       # Testing node endpoints
│   ├── executions.py    # Execution history endpoints
│   └── analysis.py      # Analysis endpoints
└── services/            # Business logic layer
    ├── graph_service.py
    ├── execution_service.py
    ├── testing_service.py
    └── analysis_service.py
```

## Integration with Backend

The API integrates with the backend LangGraph components:
- `backend/graph.py` - CallableGraph class
- `backend/node.py` - Node class
- `backend/edge.py` - Edge class
- `backend/testing_nodes/` - Testing node implementations

## Error Handling

All endpoints return standard HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses include a detail message:
```json
{
  "detail": "Error description"
}
```

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` (Next.js default)
- `http://localhost:3001`
- `http://127.0.0.1:3000`

## Health Check

```http
GET /health
```

Returns:
```json
{
  "status": "healthy",
  "service": "langgraph-testing-api"
}
```

