# Testing Guide for Streaming Execution

## Prerequisites

1. Backend API server is running:
   ```bash
   cd api
   ./start_server.sh
   ```

2. Frontend is running:
   ```bash
   cd client
   npm run dev
   ```

## Test 1: Frontend UI Test (Recommended)

This is the easiest way to test the streaming execution:

1. Open your browser to `http://localhost:3000`
2. Wait for the graph to load (you should see nodes appear on the canvas)
3. Click the "Run" button in the top bar
4. Observe:
   - Nodes highlight in blue as they execute
   - Edges animate when nodes are executing
   - Log panel shows real-time updates from backend
   - Each node shows execution time
   - Success/error status for each node

Expected behavior:
- You should see "Starting graph execution from backend..." in the logs
- Each node will show "Starting execution of node: [name]"
- When complete, shows "Node [name] completed (XXms)"
- Finally shows "✓ Graph execution completed!" with total time

## Test 2: API Test with curl

### Step 1: Load a graph
```bash
curl -X POST http://localhost:8000/api/graphs/load \
  -H "Content-Type: application/json" \
  -d '{"file_path":"../backend/graph_2.py","graph_name":"Test Graph","description":"Testing"}' \
  | python -m json.tool
```

Copy the `graph_id` from the response.

### Step 2: Test streaming execution
```bash
# Replace GRAPH_ID with the ID from step 1
curl -N -X POST "http://localhost:8000/api/graphs/GRAPH_ID/execute/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"initial_state":{}}'
```

You should see Server-Sent Events output like:
```
data: {"event_type":"start","execution_id":"...","graph_id":"...","timestamp":"...","message":"Graph execution started"}

data: {"event_type":"node_start","execution_id":"...","node_id":"step1","node_name":"step1",...}

data: {"event_type":"node_complete","execution_id":"...","node_id":"step1","status":"success","duration_ms":123.45,...}

data: {"event_type":"complete","execution_id":"...","status":"success","duration_ms":500.00,...}
```

## Test 3: Python Script Test

Run the provided test script:
```bash
cd api
python test_streaming_execution.py
```

This will:
1. Load a graph from backend
2. Stream execution events
3. Display progress with emoji indicators
4. Show summary statistics

## Expected Results

### Successful Execution
- All nodes execute in sequence
- Each node completes with status "success"
- Total execution time is displayed
- No errors in logs

### With Errors (if node fails)
- Error is reported for that specific node
- Other nodes continue to execute
- Final status shows "error"
- Error details are logged

## Debugging

### Backend Logs
Check `api` console for:
- Incoming requests
- Node execution progress
- Python exceptions or errors

### Frontend Console
Open browser DevTools and check for:
- `[useGraphEditor]` logs showing event processing
- WebSocket/SSE connection status
- Any JavaScript errors

### Common Issues

1. **"No graph loaded" error**
   - Ensure a graph was successfully loaded on frontend startup
   - Check if `currentGraphId` is set in page.tsx

2. **Connection refused**
   - Ensure API server is running on port 8000
   - Check NEXT_PUBLIC_API_URL in .env.local

3. **Nodes not executing**
   - Check if nodes have callable `data` field
   - Look for backend errors in API console

4. **Stream doesn't complete**
   - Check for backend exceptions
   - Ensure all nodes complete execution
   - Look for network errors in browser DevTools

## Performance Notes

- Each node shows actual execution time from backend
- Network latency adds minimal overhead (SSE is efficient)
- Large state objects may slow down serialization
- Consider pagination for very long execution logs

