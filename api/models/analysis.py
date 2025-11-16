"""Analysis and reporting data models."""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class TestCase(BaseModel):
    """Single test case for a test suite."""
    name: str
    description: Optional[str] = None
    input_state: Dict[str, Any]
    expected_output: Optional[Dict[str, Any]] = None
    test_type: str = "functional"


class TestSuiteRequest(BaseModel):
    """Request to run a test suite."""
    graph_id: str = Field(..., description="ID of the graph to test")
    test_cases: List[TestCase] = Field(..., description="List of test cases to run")
    config: Dict[str, Any] = Field(default_factory=dict, description="Test configuration")


class TestResult(BaseModel):
    """Result of a single test case."""
    test_name: str
    status: str  # "passed", "failed", "error"
    input_state: Dict[str, Any]
    actual_output: Dict[str, Any]
    expected_output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: float
    vulnerabilities_found: List[str] = []


class TestSuiteResponse(BaseModel):
    """Response after running a test suite."""
    suite_id: str
    graph_id: str
    total_tests: int
    passed: int
    failed: int
    errors: int
    results: List[TestResult]
    total_duration_ms: float
    executed_at: datetime = Field(default_factory=datetime.now)


class VulnerabilitySeverity(str, Enum):
    """Severity levels for vulnerabilities."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Vulnerability(BaseModel):
    """Single vulnerability finding."""
    id: str
    type: str  # "prompt_injection", "data_leak", etc.
    severity: VulnerabilitySeverity
    title: str
    description: str
    affected_nodes: List[str]
    reproduction_steps: List[str]
    test_case: Optional[str] = None
    discovered_at: datetime = Field(default_factory=datetime.now)


class VulnerabilityReport(BaseModel):
    """Report of vulnerabilities found in a graph."""
    graph_id: str
    total_vulnerabilities: int
    by_severity: Dict[str, int]
    by_type: Dict[str, int]
    vulnerabilities: List[Vulnerability]
    scan_date: datetime = Field(default_factory=datetime.now)
    recommendations: List[str] = []


class ExportFormat(str, Enum):
    """Available export formats."""
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    HTML = "html"

