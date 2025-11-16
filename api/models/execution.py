"""Execution-related data models."""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime


class ExecutionPathRequest(BaseModel):
    """Request to execute a specific path through the graph."""
    graph_id: str = Field(..., description="ID of the graph")
    node_ids: List[str] = Field(..., description="List of node IDs to execute in order")
    initial_state: Dict[str, Any] = Field(default_factory=dict, description="Initial state")
    config: Dict[str, Any] = Field(default_factory=dict, description="Execution configuration")


class NodeExecutionStep(BaseModel):
    """Single step in an execution path."""
    node_id: str
    node_name: str
    input_state: Dict[str, Any]
    output_state: Dict[str, Any]
    duration_ms: float
    status: str
    error: Optional[str] = None


class ExecutionPathResponse(BaseModel):
    """Response after executing a path."""
    execution_id: str
    graph_id: str
    node_ids: List[str]
    status: str
    steps: List[NodeExecutionStep]
    final_state: Dict[str, Any]
    total_duration_ms: float
    started_at: datetime
    completed_at: datetime


class MockStateRequest(BaseModel):
    """Request to mock state at a specific point in the graph."""
    graph_id: str = Field(..., description="ID of the graph")
    node_id: str = Field(..., description="Node ID where to set the state")
    state: Dict[str, Any] = Field(..., description="State to mock")


class MockStateResponse(BaseModel):
    """Response after mocking state."""
    graph_id: str
    node_id: str
    state: Dict[str, Any]
    message: str


class ExecutionRecord(BaseModel):
    """Record of a single execution."""
    execution_id: str
    graph_id: str
    execution_type: str  # "node", "path", "full"
    status: str
    duration_ms: float
    started_at: datetime
    completed_at: datetime
    success: bool
    error: Optional[str] = None


class ExecutionHistoryResponse(BaseModel):
    """Response with execution history."""
    executions: List[ExecutionRecord]
    total: int
    page: int
    page_size: int


class ExecutionDetailsResponse(BaseModel):
    """Detailed information about a specific execution."""
    execution_id: str
    graph_id: str
    execution_type: str
    status: str
    initial_state: Dict[str, Any]
    final_state: Dict[str, Any]
    steps: List[NodeExecutionStep]
    logs: List[Dict[str, Any]]
    duration_ms: float
    started_at: datetime
    completed_at: datetime
    success: bool
    error: Optional[str] = None


class StreamExecutionEvent(BaseModel):
    """Event sent during streaming execution."""
    event_type: str = Field(..., description="Type of event: start, node_start, node_complete, complete, error")
    execution_id: str
    graph_id: str
    timestamp: datetime
    node_id: Optional[str] = None
    node_name: Optional[str] = None
    status: Optional[str] = None
    input_state: Optional[Dict[str, Any]] = None
    output_state: Optional[Dict[str, Any]] = None
    duration_ms: Optional[float] = None
    error: Optional[str] = None
    message: Optional[str] = None
