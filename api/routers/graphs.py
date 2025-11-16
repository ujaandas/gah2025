"""Graph management endpoints."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
import json

from models.graph import (
    GraphLoadRequest,
    GraphLoadResponse,
    GraphResponse,
    GraphListResponse,
    GraphListItem,
    GraphExecuteRequest,
    GraphExecuteResponse,
)
from services.graph_service import get_graph_service
from services.execution_service import get_execution_service

router = APIRouter(prefix="/api/graphs", tags=["graphs"])


@router.post("/load", response_model=GraphLoadResponse, status_code=status.HTTP_201_CREATED)
async def load_graph(request: GraphLoadRequest):
    """
    Load a LangGraph from code, file, or module.
    
    Provide one of:
    - code: Python code string containing LangGraph definition
    - file_path: Path to file containing LangGraph
    - module_path: Module path to import LangGraph from
    """
    try:
        graph_service = get_graph_service()
        response = graph_service.load_graph(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to load graph: {str(e)}"
        )


@router.get("", response_model=GraphListResponse)
async def list_graphs():
    """
    List all loaded graphs.
    """
    graph_service = get_graph_service()
    graphs = graph_service.list_graphs()
    return GraphListResponse(graphs=graphs, total=len(graphs))


@router.get("/{graph_id}", response_model=GraphResponse)
async def get_graph(graph_id: str):
    """
    Get details of a specific graph.
    """
    graph_service = get_graph_service()
    graph = graph_service.get_graph(graph_id)
    
    if graph is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph not found: {graph_id}"
        )
    
    return graph


@router.post("/{graph_id}/execute", response_model=GraphExecuteResponse)
async def execute_graph(graph_id: str, request: GraphExecuteRequest):
    """
    Execute the entire graph with the provided initial state.
    """
    try:
        graph_service = get_graph_service()
        execution_service = get_execution_service()
        
        response = execution_service.execute_full_graph(
            graph_id,
            request,
            graph_service
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute graph: {str(e)}"
        )


@router.post("/{graph_id}/execute/stream")
async def stream_execute_graph(graph_id: str, request: GraphExecuteRequest):
    """
    Execute the entire graph with streaming updates via Server-Sent Events.
    
    Returns a stream of events:
    - start: Execution started
    - node_start: Node execution started
    - node_complete: Node execution completed
    - complete: Graph execution completed
    - error: Error occurred
    """
    graph_service = get_graph_service()
    execution_service = get_execution_service()
    
    # Verify graph exists
    if graph_id not in graph_service.graphs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph not found: {graph_id}"
        )
    
    async def event_generator():
        """Generate Server-Sent Events."""
        try:
            for event in execution_service.stream_full_graph_execution(
                graph_id,
                request,
                graph_service
            ):
                # Convert event to dict and then to JSON
                event_dict = event.dict()
                # Convert datetime to ISO format string
                if 'timestamp' in event_dict and event_dict['timestamp']:
                    event_dict['timestamp'] = event_dict['timestamp'].isoformat()
                
                # Format as SSE
                yield f"data: {json.dumps(event_dict)}\n\n"
        except Exception as e:
            # Send error event
            error_event = {
                "event_type": "error",
                "error": str(e),
                "message": f"Stream error: {str(e)}"
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


@router.delete("/{graph_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_graph(graph_id: str):
    """
    Delete a graph.
    """
    graph_service = get_graph_service()
    
    if graph_id not in graph_service.graphs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph not found: {graph_id}"
        )
    
    del graph_service.graphs[graph_id]
    return None

