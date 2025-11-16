"""Graph-related data models."""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime


class GraphLoadRequest(BaseModel):
    """Request to load a LangGraph."""
    code: Optional[str] = Field(None, description="Python code containing LangGraph definition")
    file_path: Optional[str] = Field(None, description="Path to file containing LangGraph")
    module_path: Optional[str] = Field(None, description="Module path to import LangGraph from")
    graph_name: str = Field("workflow", description="Name for the graph")
    description: Optional[str] = Field(None, description="Description of the graph")


class NodeInfo(BaseModel):
    """Information about a node in the graph."""
    id: str
    name: str
    node_type: str
    is_testing: bool = False
    metadata: Dict[str, Any] = {}


class EdgeInfo(BaseModel):
    """Information about an edge in the graph."""
    source: str
    target: str
    conditional: bool = False
    metadata: Dict[str, Any] = {}


class GraphStructure(BaseModel):
    """Structure of a graph."""
    nodes: Dict[str, NodeInfo]
    edges: List[EdgeInfo]
    start_nodes: List[str]
    end_nodes: List[str]


class GraphLoadResponse(BaseModel):
    """Response after loading a graph."""
    graph_id: str
    name: str
    description: Optional[str]
    structure: GraphStructure
    created_at: datetime = Field(default_factory=datetime.now)


class GraphResponse(BaseModel):
    """Response with graph details."""
    graph_id: str
    name: str
    description: Optional[str]
    structure: GraphStructure
    created_at: datetime
    last_executed: Optional[datetime] = None


class GraphListItem(BaseModel):
    """Summary of a graph in list view."""
    graph_id: str
    name: str
    description: Optional[str]
    node_count: int
    edge_count: int
    created_at: datetime
    last_executed: Optional[datetime] = None


class GraphListResponse(BaseModel):
    """Response with list of graphs."""
    graphs: List[GraphListItem]
    total: int


class GraphExecuteRequest(BaseModel):
    """Request to execute a full graph."""
    initial_state: Dict[str, Any] = Field(default_factory=dict, description="Initial state for the graph")
    config: Dict[str, Any] = Field(default_factory=dict, description="Execution configuration")


class GraphExecuteResponse(BaseModel):
    """Response after executing a graph."""
    execution_id: str
    graph_id: str
    status: str
    final_state: Dict[str, Any]
    execution_history: List[Dict[str, Any]]
    duration_ms: float
    started_at: datetime
    completed_at: datetime

