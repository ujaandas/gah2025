"""Node execution endpoints."""

from fastapi import APIRouter, HTTPException, status

from models.node import (
    NodeExecuteRequest,
    NodeExecuteResponse,
    NodeStateResponse,
)
from services.graph_service import get_graph_service
from services.execution_service import get_execution_service

router = APIRouter(prefix="/api/nodes", tags=["nodes"])


@router.post("/execute", response_model=NodeExecuteResponse)
async def execute_node(request: NodeExecuteRequest):
    """
    Execute a single node with custom inputs.
    
    This allows you to test individual nodes in isolation without running
    the entire graph. You can provide:
    - input_state: The state to pass to the node
    - mock_previous_state: Mock state from previous nodes in the graph
    """
    try:
        graph_service = get_graph_service()
        execution_service = get_execution_service()
        
        response = execution_service.execute_node(request, graph_service)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute node: {str(e)}"
        )


@router.get("/{graph_id}/{node_id}/state", response_model=NodeStateResponse)
async def get_node_state(graph_id: str, node_id: str):
    """
    Get the current state at a specific node.
    """
    graph_service = get_graph_service()
    
    # Get the graph
    graph = graph_service.get_graph_instance(graph_id)
    if graph is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph not found: {graph_id}"
        )
    
    # Get the node
    node = graph.nodes.get(node_id)
    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node not found: {node_id}"
        )
    
    # Get node-specific output from execution history
    node_output = {}
    if node.execution_history and len(node.execution_history) > 0:
        # Get the latest execution output
        latest_execution = node.execution_history[-1]
        if latest_execution.get("success") and "output" in latest_execution:
            node_output = latest_execution["output"]
    
    return NodeStateResponse(
        graph_id=graph_id,
        node_id=node_id,
        node_name=node.name,
        current_state=node_output,  # Return node-specific output instead of global state
        execution_count=node.execution_count,
        last_executed=node.last_executed,
    )

