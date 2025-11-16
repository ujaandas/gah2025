# LLM Analysis Integration for Test Page

## Overview

The test page now includes automatic LLM-powered analysis after graph execution. When you run a graph, the system will automatically generate a comprehensive security analysis using AI.

## What Was Added

### Frontend Changes (client/src/app/test/page.tsx)

1. **AnalysisPanel Component**: Imported and integrated the existing analysis panel
2. **State Management**: Added tracking for:
   - `lastExecutionId`: Stores the ID of the most recent execution
   - `isAnalysisPanelOpen`: Controls the visibility of the analysis panel

3. **Automatic Analysis Triggering**: After graph execution completes:
   - The execution ID is captured
   - Analysis panel automatically opens
   - A "View Analysis" button appears in the top bar

4. **User Experience**:
   - Graph executes as normal with streaming updates
   - When execution completes, analysis panel slides in from the right
   - Analysis is automatically generated using your LLM API
   - Results show:
     - Risk score (0-100)
     - Security summary
     - Detected vulnerabilities
     - Security issues
     - Recommendations
     - Detailed analysis

### Backend (Already Configured)

The backend LLM analysis was already fully implemented:
- `/api/analysis/llm-analysis` endpoint (api/routers/analysis.py)
- Analysis service with LLM integration (api/services/analysis_service.py)
- LLM client for calling your team's API (backend/llm_client.py)

## How to Use

### 1. Configure LLM API Credentials

Create or update `/backend/.env` with your team credentials:

```bash
TEAM_ID=your_team_id
API_TOKEN=your_api_token
```

**Important**: Never commit the `.env` file to git (it's already in `.gitignore`).

### 2. Start the Application

Make sure both backend and frontend are running:

```bash
# Terminal 1 - Backend
cd api
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd client
npm run dev
```

### 3. Use the Test Page

1. Navigate to `/test` page
2. Upload an agent file (or use any file to enter demo mode)
3. Click the "Execute" button to run the graph
4. Wait for execution to complete (watch the streaming logs)
5. **Analysis panel will automatically open** with AI-powered insights

### 4. View Analysis Anytime

After an execution completes, you can:
- Click the "View Analysis" button in the top bar
- See the risk score, vulnerabilities, and recommendations
- Expand "Detailed Analysis" for comprehensive insights
- Click "Regenerate Analysis" to get a fresh analysis

## Features

### Automatic Analysis Generation

The analysis is generated automatically using your LLM API with the following information:
- Graph structure and description
- Execution steps and results
- Node outputs and errors
- Final state of the execution

### Analysis Contents

1. **Summary**: Brief 2-3 sentence overview of what happened
2. **Risk Score**: Numerical score from 0-100
   - 0-24: Low risk (green)
   - 25-49: Medium risk (yellow)
   - 50-74: High risk (orange)
   - 75-100: Critical risk (red)
3. **Vulnerabilities**: Specific security vulnerabilities detected
4. **Security Issues**: Broader security concerns
5. **Recommendations**: Actionable suggestions for improvement
6. **Detailed Analysis**: Comprehensive review of the execution

### Visual Feedback

- Risk score with color-coded progress bar
- Animated appearance with smooth transitions
- Collapsible detailed analysis section
- Success/error/warning indicators
- Execution logs include analysis completion message

## API Details

### Request Format

The frontend sends this request to generate analysis:

```json
{
  "graph_id": "uuid-of-graph",
  "execution_id": "uuid-of-execution",
  "focus_areas": ["security", "vulnerabilities", "prompt_injection"]
}
```

### Response Format

```json
{
  "analysis_id": "uuid",
  "graph_id": "uuid",
  "execution_id": "uuid",
  "summary": "Brief summary of execution",
  "vulnerabilities": ["vulnerability 1", "vulnerability 2"],
  "security_issues": ["issue 1", "issue 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "detailed_analysis": "Comprehensive analysis text...",
  "risk_score": 65,
  "generated_at": "2025-11-16T13:21:00Z"
}
```

## Troubleshooting

### Issue: "Missing graph ID or execution ID"

**Solution**: Make sure the graph executes successfully before trying to view analysis. The analysis requires both IDs to be available.

### Issue: "Failed to generate analysis" or timeout

**Solutions**:
1. Check that TEAM_ID and API_TOKEN are correctly set in `/backend/.env`
2. Verify network connectivity to the LLM API endpoint
3. Check the backend logs for detailed error messages
4. Try regenerating the analysis (temporary API issues)

### Issue: Analysis panel doesn't open automatically

**Solution**: Check the browser console for errors. The panel should open when `lastExecutionId` is set. You can manually open it using the "View Analysis" button.

### Issue: LLM API not available

The system will show an error if the LLM API is not configured. The analysis service will return a descriptive error message. You can still:
- View execution logs
- Inspect node data
- Export results

## Testing Without LLM API

If you want to test the UI without configuring the LLM API, you can:

1. Start the backend without credentials (analysis will fail gracefully)
2. Run the graph execution
3. Try to open analysis - you'll see an error message
4. This verifies the UI components work correctly

For full testing with actual analysis:
1. Add your TEAM_ID and API_TOKEN to `/backend/.env`
2. Test with: `cd backend && python test_llm_integration.py`
3. Run a graph execution on the test page
4. Verify analysis is generated automatically

## Code Architecture

### Component Flow

```
Test Page (page.tsx)
  ├─> useGraphEditor hook
  │   └─> handleRun() with onExecutionComplete callback
  │       └─> Sets lastExecutionId
  │
  ├─> useEffect on lastExecutionId change
  │   └─> Opens AnalysisPanel
  │
  └─> AnalysisPanel component
      ├─> Auto-fetches analysis on mount
      ├─> Calls /api/analysis/llm-analysis
      └─> Displays results
```

### Key State Management

```typescript
// Execution tracking
const [lastExecutionId, setLastExecutionId] = useState<string | null>(null);
const { lastExecutionId: hookLastExecutionId } = useGraphEditor();

// Auto-open on new execution
useEffect(() => {
  if (hookLastExecutionId && hookLastExecutionId !== lastExecutionId) {
    setLastExecutionId(hookLastExecutionId);
    setIsAnalysisPanelOpen(true);
  }
}, [hookLastExecutionId, lastExecutionId]);

// Manual open via button
<TopBar
  onViewAnalysis={() => setIsAnalysisPanelOpen(true)}
  hasExecutionCompleted={!!lastExecutionId}
/>
```

## Model Selection

The analysis service uses the default model from the LLM client:
- **Default**: `us.anthropic.claude-3-5-sonnet-20241022-v2:0` (balanced quality/speed)

You can modify the model in `api/services/analysis_service.py` line 471:

```python
llm_response = llm_client.call(
    prompt=prompt,
    max_tokens=2048,
    temperature=0.3,
    model="us.anthropic.claude-3-5-haiku-20241022-v1:0"  # Faster
)
```

Available models are listed in `backend/LLM_API_MIGRATION.md`.

## Performance

- Analysis typically takes 2-5 seconds depending on:
  - Execution complexity (number of steps)
  - Graph size
  - LLM model selected
  - API response time

- The UI shows a loading spinner during analysis generation
- Analysis is cached by analysis_id for quick retrieval

## Future Enhancements

Possible improvements:
1. Allow users to customize focus areas in the UI
2. Export analysis reports (PDF, HTML)
3. Compare analyses across multiple executions
4. Add analysis history view
5. Integrate analysis results into testing workflow
6. Add batch analysis for multiple test runs

## Related Files

### Frontend
- `client/src/app/test/page.tsx` - Main test page with analysis integration
- `client/src/components/AnalysisPanel.tsx` - Analysis panel component
- `client/src/components/TopBar.tsx` - Top bar with "View Analysis" button
- `client/src/hooks/useGraphEditor.tsx` - Graph execution hook

### Backend
- `api/routers/analysis.py` - Analysis API endpoints
- `api/services/analysis_service.py` - Analysis service with LLM integration
- `api/models/analysis.py` - Analysis data models
- `backend/llm_client.py` - LLM API client

### Documentation
- `backend/LLM_API_MIGRATION.md` - LLM API setup and model details
- `LLM_ANALYSIS_FEATURE.md` - Original LLM analysis feature documentation

## Summary

The test page now provides automatic, AI-powered analysis of every graph execution. This helps users:
- Quickly identify security issues
- Understand execution behavior
- Get actionable recommendations
- Track risk over time

The integration is seamless and works automatically - just run a graph and the analysis appears!

