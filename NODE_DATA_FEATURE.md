# Node Data Display Feature

## Overview
This feature allows users to click on any node in the graph to view its execution data and state information.

## How It Works

### Frontend Components

1. **NodeDataPanel Component** (`client/src/components/NodeDataPanel.tsx`)
   - A slide-in panel that displays node information
   - Shows execution count, last execution time, current state, and node details
   - Automatically fetches data from the backend when opened
   - Can be closed by clicking the backdrop, close button, or pressing Escape

2. **Enhanced Node Click Handler** (`client/src/app/page.tsx`)
   - When a node is clicked, it:
     - Selects the node (existing behavior)
     - Opens the Node Data Panel
     - Fetches node state from the backend API

3. **API Client Method** (`client/src/lib/api/graphApi.ts`)
   - New `getNodeState()` method that calls the backend API
   - Returns node execution data including state and execution history

### Backend API

**Endpoint**: `GET /api/nodes/{graph_id}/{node_id}/state`

**Response**:
```json
{
  "graph_id": "string",
  "node_id": "string",
  "node_name": "string",
  "current_state": {},
  "execution_count": 0,
  "last_executed": "2025-11-16T10:30:00"
}
```

## Usage

1. **Before Execution**:
   - Click on any node
   - The panel opens showing "No data yet. Run the graph to populate."
   - Execution count will be 0

2. **After Execution**:
   - Run the graph using the "Run" button
   - Click on any executed node
   - The panel displays:
     - Execution count
     - Last execution timestamp
     - Current state data (JSON format)
     - Node metadata

3. **Closing the Panel**:
   - Click the X button in the top right
   - Click outside the panel (on the backdrop)
   - Press the Escape key

## Features

- **Real-time Data**: Fetches fresh data from backend each time a node is clicked
- **Error Handling**: Shows clear error messages if data fetch fails
- **Loading States**: Displays loading spinner while fetching data
- **Responsive Design**: Panel slides in from the right with smooth animations
- **Keyboard Support**: Press Escape to close the panel
- **JSON Formatting**: State data is displayed in a formatted, readable JSON view

## Implementation Details

### State Management
- Uses React hooks for local state management
- Panel state is managed in the main page component
- Fetches data on-demand when panel opens

### API Integration
- Uses the existing `graphApiClient` singleton
- Follows the same error handling patterns as other API calls
- Returns properly typed responses

### Styling
- Uses Tailwind CSS for consistent styling
- Gradient header for visual appeal
- Color-coded sections for different types of information
- Monospace font for JSON and IDs

## Testing

To test the feature:

1. Start the backend API: `cd api && bash start_server.sh`
2. Start the frontend: `cd client && npm run dev`
3. Open http://localhost:3000
4. Click on any node (before execution) - should show "no data yet"
5. Click the "Run" button to execute the graph
6. Click on nodes again - should show execution data and state

## Future Enhancements

Potential improvements:
- Add execution history timeline
- Show input vs output state diff
- Add ability to edit/mock state directly from panel
- Show node performance metrics (execution time, etc.)
- Add export functionality for node data

