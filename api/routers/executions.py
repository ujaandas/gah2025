"""Execution history and logging endpoints."""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional

from models.execution import (
    ExecutionPathRequest,
    ExecutionPathResponse,
    ExecutionHistoryResponse,
    ExecutionDetailsResponse,
    MockStateRequest,
    MockStateResponse,
)
from services.execution_service import get_execution_service
from services.graph_service import get_graph_service

router = APIRouter(prefix="/api/executions", tags=["executions"])


@router.post("/path", response_model=ExecutionPathResponse)
async def execute_path(request: ExecutionPathRequest):
    """
    Execute a specific path through the graph.
    
    This allows you to test a sequence of nodes without running the entire graph.
    Provide a list of node IDs to execute in order.
    """
    try:
        execution_service = get_execution_service()
        graph_service = get_graph_service()
        
        response = execution_service.execute_path(request, graph_service)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute path: {str(e)}"
        )


@router.get("", response_model=ExecutionHistoryResponse)
async def get_execution_history(
    graph_id: Optional[str] = Query(None, description="Filter by graph ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page")
):
    """
    Get execution history.
    
    Optionally filter by graph_id to see executions for a specific graph.
    Results are paginated.
    """
    execution_service = get_execution_service()
    return execution_service.get_execution_history(graph_id, page, page_size)


@router.get("/{execution_id}", response_model=ExecutionDetailsResponse)
async def get_execution_details(execution_id: str):
    """
    Get detailed information about a specific execution.
    
    Includes:
    - Input and output states
    - Step-by-step execution trace
    - Logs and timing information
    - Any errors encountered
    """
    execution_service = get_execution_service()
    
    details = execution_service.get_execution_details(execution_id)
    if details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution not found: {execution_id}"
        )
    
    return details


@router.post("/mock-state", response_model=MockStateResponse)
async def mock_state(request: MockStateRequest):
    """
    Mock the state at a specific point in the graph.
    
    This allows you to set up specific conditions for testing without
    needing to execute previous nodes. The mocked state will be used
    in subsequent node executions.
    """
    try:
        execution_service = get_execution_service()
        graph_service = get_graph_service()
        
        # Verify graph exists
        graph = graph_service.get_graph_instance(request.graph_id)
        if graph is None:
            raise ValueError(f"Graph not found: {request.graph_id}")
        
        # Verify node exists
        if request.node_id not in graph.nodes:
            raise ValueError(f"Node not found: {request.node_id}")
        
        response = execution_service.mock_state(request)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mock state: {str(e)}"
        )


@router.delete("/mock-state/{graph_id}/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_mocked_state(graph_id: str, node_id: str):
    """
    Clear mocked state for a specific node.
    """
    execution_service = get_execution_service()
    
    if graph_id in execution_service.mocked_states:
        if node_id in execution_service.mocked_states[graph_id]:
            del execution_service.mocked_states[graph_id][node_id]
    
    return None

