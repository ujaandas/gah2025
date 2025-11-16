"""Testing node-related data models."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum


class TestingNodeType(str, Enum):
    """Types of testing nodes available."""
    PROMPT_INJECTION = "prompt_injection"
    FUZZER = "fuzzer"
    VALIDATOR = "validator"
    MOCK = "mock"


class TestingNodeAddRequest(BaseModel):
    """Request to add a testing node to a graph."""
    graph_id: str = Field(..., description="ID of the graph to add the node to")
    node_type: TestingNodeType = Field(..., description="Type of testing node")
    position: str = Field(..., description="Position in graph (e.g., 'before:supervisor')")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration for the testing node")
    name: Optional[str] = Field(None, description="Custom name for the node")


class TestingNodeAddResponse(BaseModel):
    """Response after adding a testing node."""
    node_id: str
    graph_id: str
    node_type: str
    position: str
    config: Dict[str, Any]
    message: str


class TestingNodeTemplate(BaseModel):
    """Template for a testing node type."""
    node_type: TestingNodeType
    display_name: str
    description: str
    icon: str
    default_config: Dict[str, Any]
    config_schema: Dict[str, Any]


class TestingNodeConfigRequest(BaseModel):
    """Request to configure a testing node."""
    config: Dict[str, Any] = Field(..., description="New configuration for the testing node")


class TestingNodeConfigResponse(BaseModel):
    """Response after configuring a testing node."""
    node_id: str
    graph_id: str
    config: Dict[str, Any]
    message: str

