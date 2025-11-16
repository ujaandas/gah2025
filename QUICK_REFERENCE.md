# Quick Reference - Streaming Execution

## 🚀 Quick Start

```bash
# Terminal 1: Start Backend
cd api && ./start_server.sh

# Terminal 2: Start Frontend
cd client && npm run dev

# Browser: Open http://localhost:3000
# Click "Run" button → Watch live execution! ✨
```

## 📡 New API Endpoint

```
POST /api/graphs/{graph_id}/execute/stream
Content-Type: application/json
Accept: text/event-stream

Body: {"initial_state": {}}

Returns: Server-Sent Events stream
```

## 🎯 Event Types

| Event Type | When | Contains |
|------------|------|----------|
| `start` | Execution begins | execution_id, graph_id, initial_state |
| `node_start` | Node starts executing | node_id, node_name, input_state |
| `node_complete` | Node finishes | node_id, status, output_state, duration_ms, error? |
| `complete` | All done | final_state, duration_ms, status |
| `error` | Something broke | error, message |

## 💻 Code Examples

### Backend - Stream Events
```python
for event in execution_service.stream_full_graph_execution(graph_id, request, graph_service):
    yield event  # StreamExecutionEvent
```

### Frontend - Receive Events
```typescript
graphApiClient.streamExecuteGraph(
  graphId,
  { initial_state: {} },
  (event) => {
    console.log('Event:', event.event_type);
    // Handle event
  }
);
```

## 🔍 Debugging

### Check API Health
```bash
curl http://localhost:8000/health
```

### Test Stream Directly
```bash
# 1. Get graph ID
curl -X POST http://localhost:8000/api/graphs/load \
  -H "Content-Type: application/json" \
  -d '{"file_path":"../backend/graph_2.py","graph_name":"Test","description":"Test"}'

# 2. Stream execution
curl -N -X POST http://localhost:8000/api/graphs/GRAPH_ID/execute/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{}'
```

### Frontend Console
```javascript
// Look for these logs:
[useGraphEditor] handleRun called
[useGraphEditor] Starting streaming execution...
[useGraphEditor] Received event: { event_type: 'start', ... }
```

## 📁 Key Files

### Backend
- `api/models/execution.py` - Event models
- `api/services/execution_service.py` - Stream generator
- `api/routers/graphs.py` - SSE endpoint

### Frontend
- `client/src/lib/api/graphApi.ts` - API client
- `client/src/hooks/useGraphEditor.tsx` - Execution logic
- `client/src/app/page.tsx` - Integration

## ✨ Features

✅ Real-time node execution updates  
✅ Live timing data from backend  
✅ Visual node highlighting  
✅ Animated edges  
✅ Error reporting  
✅ Automatic cleanup  

## 📚 Documentation

- `IMPLEMENTATION_SUMMARY.md` - Overview & architecture
- `STREAMING_EXECUTION_IMPLEMENTATION.md` - Technical details
- `TESTING_GUIDE.md` - Testing instructions
- `api/test_streaming_execution.py` - Automated test

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| "No graph loaded" | Ensure graph loads on frontend startup |
| Connection refused | Check API server is running on port 8000 |
| Nodes don't execute | Verify nodes have callable `data` field |
| Stream hangs | Check backend logs for exceptions |

## 🎨 UI Indicators

- 🔵 **Blue glow** = Node executing
- ✅ **Green log** = Success
- ❌ **Red log** = Error
- 📊 **Timing** = Shown in milliseconds

## 🔗 URLs

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

**Status**: ✅ Fully Implemented & Ready  
**Version**: 1.0  
**Last Updated**: November 2025

