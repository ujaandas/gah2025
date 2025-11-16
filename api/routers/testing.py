"""Testing node endpoints."""

from fastapi import APIRouter, HTTPException, status
from typing import List

from models.testing import (
    TestingNodeAddRequest,
    TestingNodeAddResponse,
    TestingNodeTemplate,
    TestingNodeConfigRequest,
    TestingNodeConfigResponse,
)
from services.testing_service import get_testing_service
from services.graph_service import get_graph_service

router = APIRouter(prefix="/api/testing-nodes", tags=["testing"])


@router.get("/templates", response_model=List[TestingNodeTemplate])
async def get_testing_node_templates():
    """
    Get all available testing node templates.
    
    Returns information about each type of testing node that can be added,
    including their configuration options.
    """
    testing_service = get_testing_service()
    return testing_service.get_templates()


@router.post("", response_model=TestingNodeAddResponse, status_code=status.HTTP_201_CREATED)
async def add_testing_node(request: TestingNodeAddRequest):
    """
    Add a testing node to a graph.
    
    Testing nodes can be inserted at specific positions in the graph to:
    - Inject malicious prompts (prompt_injection)
    - Fuzz inputs (fuzzer)
    - Validate outputs (validator)
    - Mock expensive operations (mock)
    
    Position format:
    - "before:node_id" - Insert before the specified node
    - "after:node_id" - Insert after the specified node
    """
    try:
        testing_service = get_testing_service()
        graph_service = get_graph_service()
        
        response = testing_service.add_testing_node(request, graph_service)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add testing node: {str(e)}"
        )


@router.put("/{graph_id}/{node_id}", response_model=TestingNodeConfigResponse)
async def configure_testing_node(
    graph_id: str,
    node_id: str,
    request: TestingNodeConfigRequest
):
    """
    Update the configuration of an existing testing node.
    """
    try:
        testing_service = get_testing_service()
        
        response = testing_service.configure_testing_node(node_id, graph_id, request)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to configure testing node: {str(e)}"
        )


@router.delete("/{graph_id}/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_testing_node(graph_id: str, node_id: str):
    """
    Remove a testing node from a graph.
    """
    testing_service = get_testing_service()
    graph_service = get_graph_service()
    
    # Get the graph
    graph = graph_service.get_graph_instance(graph_id)
    if graph is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph not found: {graph_id}"
        )
    
    # Check if node exists and is a testing node
    if node_id not in testing_service.testing_nodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Testing node not found: {node_id}"
        )
    
    # Remove from graph
    if node_id in graph.nodes:
        del graph.nodes[node_id]
    
    # Remove edges connected to this node
    graph.edges = [e for e in graph.edges if e.source != node_id and e.target != node_id]
    graph._update_start_end_nodes()
    
    # Remove from tracking
    del testing_service.testing_nodes[node_id]
    if graph_id in testing_service.graph_testing_nodes:
        testing_service.graph_testing_nodes[graph_id] = [
            n for n in testing_service.graph_testing_nodes[graph_id] if n != node_id
        ]
    
    return None

