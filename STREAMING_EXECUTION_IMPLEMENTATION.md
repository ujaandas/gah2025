# Streaming Execution Implementation

## Overview

The run system has been updated to integrate with the backend using Server-Sent Events (SSE) for real-time execution updates. The frontend now receives live updates from the backend as each node executes, providing a more accurate and responsive execution experience.

## Architecture

### Backend Changes

#### 1. Execution Models (`api/models/execution.py`)
- Added `StreamExecutionEvent` model to represent execution events
- Event types: `start`, `node_start`, `node_complete`, `complete`, `error`
- Each event contains execution metadata, node information, timing, and status

#### 2. Execution Service (`api/services/execution_service.py`)
- Added `stream_full_graph_execution()` generator function
- Yields execution events as the graph runs
- Executes nodes sequentially from the backend graph
- Captures and reports errors while continuing execution
- Stores execution history for later retrieval

#### 3. API Router (`api/routers/graphs.py`)
- Added `POST /api/graphs/{graph_id}/execute/stream` endpoint
- Returns Server-Sent Events stream
- Converts events to SSE format (`data: {JSON}\n\n`)
- Proper headers for SSE (Cache-Control, Connection, X-Accel-Buffering)

### Frontend Changes

#### 1. API Client (`client/src/lib/api/graphApi.ts`)
- Added `StreamExecutionEvent` interface
- Added `GraphExecuteRequest` interface
- Added `streamExecuteGraph()` method
- Uses Fetch API with ReadableStream for SSE parsing
- Returns cleanup function to abort the stream
- Handles event parsing and error conditions

#### 2. Graph Editor Hook (`client/src/hooks/useGraphEditor.tsx`)
- Updated `handleRun()` to accept `graphId` parameter
- Replaced mock execution with real streaming API calls
- Processes different event types and updates UI accordingly:
  - `start`: Shows execution start message
  - `node_start`: Adds node to executing list, shows start log
  - `node_complete`: Removes node from executing list, shows result with timing
  - `complete`: Shows completion message with total time
  - `error`: Shows error messages and stops execution
- Added cleanup effect to abort stream on component unmount
- Maintains stream cleanup reference for proper resource management

#### 3. Main Page (`client/src/app/page.tsx`)
- Updated `handleRun` call to pass `currentGraphId`
- Logs graph ID for debugging

## Event Flow

```
User clicks "Run" button
    ↓
Frontend: handleRun() called with graphId
    ↓
Frontend: Call graphApiClient.streamExecuteGraph()
    ↓
Backend: POST /api/graphs/{graph_id}/execute/stream
    ↓
Backend: stream_full_graph_execution() generator starts
    ↓
Backend: Yields "start" event
    ↓
Frontend: Receives event, shows "Graph execution started"
    ↓
For each node in graph:
    Backend: Yields "node_start" event
        ↓
    Frontend: Adds node to executing list, shows log
        ↓
    Backend: Executes node.execute(state)
        ↓
    Backend: Yields "node_complete" event with results/timing
        ↓
    Frontend: Removes node from executing list, shows result
    ↓
Backend: Yields "complete" event
    ↓
Frontend: Shows completion message, cleans up
```

## Event Types

### start
- Sent when graph execution begins
- Contains: execution_id, graph_id, initial_state

### node_start
- Sent when a node begins execution
- Contains: node_id, node_name, input_state

### node_complete
- Sent when a node finishes (success or error)
- Contains: node_id, node_name, status, output_state, duration_ms, error (if any)

### complete
- Sent when entire graph execution finishes
- Contains: final_state, duration_ms, status

### error
- Sent when a critical error occurs
- Contains: error message and details

## Visual Feedback

The frontend provides several forms of visual feedback:

1. **Node Highlighting**: Executing nodes are highlighted with blue border and glow effect
2. **Edge Animation**: Edges connecting to executing nodes are animated
3. **Log Panel**: Real-time logs show execution progress, timing, and messages
4. **Run Button**: Disabled during execution to prevent concurrent runs

## Error Handling

- Backend continues executing remaining nodes even if one fails
- Errors are reported as events with details
- Frontend displays errors in log panel with red highlighting
- Stream is properly cleaned up on errors or completion
- Component unmount aborts any active streams

## Testing the Implementation

### 1. Start the Backend API
```bash
cd api
./start_server.sh
```

### 2. Start the Frontend
```bash
cd client
npm run dev
```

### 3. Load a Graph
- The frontend automatically loads `backend/graph_2.py` on startup
- Or use the API to load a different graph

### 4. Execute the Graph
- Click the "Run" button in the top bar
- Watch the nodes highlight as they execute
- View real-time logs in the log panel
- See timing information for each node

### 5. Monitor Backend Logs
- Backend console shows execution progress
- Check for any errors or warnings

## Benefits

1. **Real-time Updates**: Frontend updates instantly as backend executes
2. **Accurate Execution**: Uses actual backend code, not mock/simulation
3. **Better Debugging**: See exactly what's happening in backend
4. **Performance Metrics**: Real timing data from backend execution
5. **Error Visibility**: Immediate feedback on execution failures
6. **Scalable**: SSE is efficient for one-way streaming data

## Future Enhancements

Potential improvements:
- Add execution cancellation (stop button)
- Support for graph execution with custom initial state
- Parallel node execution with proper dependency tracking
- Execution history viewer with replay capability
- Performance profiling and bottleneck detection
- Node output inspection and state diff viewing

