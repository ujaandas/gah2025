"""Service for execution operations."""

import uuid
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from models.node import NodeExecuteRequest, NodeExecuteResponse
from models.execution import (
    ExecutionPathRequest,
    ExecutionPathResponse,
    NodeExecutionStep,
    ExecutionRecord,
    ExecutionHistoryResponse,
    ExecutionDetailsResponse,
    MockStateRequest,
    MockStateResponse,
)
from models.graph import GraphExecuteRequest, GraphExecuteResponse


class ExecutionService:
    """Service for managing executions."""

    def __init__(self):
        self.executions: Dict[str, Dict[str, Any]] = {}  # execution_id -> execution data
        self.mocked_states: Dict[str, Dict[str, Any]] = {}  # graph_id -> {node_id -> state}

    def execute_node(
        self,
        request: NodeExecuteRequest,
        graph_service
    ) -> NodeExecuteResponse:
        """Execute a single node."""
        execution_id = str(uuid.uuid4())
        start_time = time.time()

        # Get the graph
        graph = graph_service.get_graph_instance(request.graph_id)
        if graph is None:
            raise ValueError(f"Graph not found: {request.graph_id}")

        # Get the node
        node = graph.nodes.get(request.node_id)
        if node is None:
            raise ValueError(f"Node not found: {request.node_id}")

        # Prepare state
        state = request.input_state.copy()
        if request.mock_previous_state:
            state.update(request.mock_previous_state)

        # Check for mocked state
        if request.graph_id in self.mocked_states:
            if request.node_id in self.mocked_states[request.graph_id]:
                state.update(self.mocked_states[request.graph_id][request.node_id])

        # Execute the node
        logs = []
        output_state = {}
        error = None
        status = "success"

        try:
            if node.data is not None and callable(node.data):
                output_state = node.execute(state)
                logs.append(f"Node {node.name} executed successfully")
            else:
                logs.append(f"Node {node.name} has no callable data, passing through state")
                output_state = state.copy()
        except Exception as e:
            status = "error"
            error = str(e)
            logs.append(f"Error executing node {node.name}: {error}")
            output_state = state.copy()

        duration_ms = (time.time() - start_time) * 1000

        # Store execution
        self.executions[execution_id] = {
            "execution_id": execution_id,
            "graph_id": request.graph_id,
            "node_id": request.node_id,
            "execution_type": "node",
            "status": status,
            "input_state": state,
            "output_state": output_state,
            "logs": logs,
            "duration_ms": duration_ms,
            "started_at": datetime.now(),
            "completed_at": datetime.now(),
            "success": status == "success",
            "error": error,
        }

        # Update graph last executed
        graph_service.update_last_executed(request.graph_id)

        return NodeExecuteResponse(
            execution_id=execution_id,
            graph_id=request.graph_id,
            node_id=request.node_id,
            node_name=node.name,
            status=status,
            input_state=state,
            output_state=output_state,
            logs=logs,
            duration_ms=duration_ms,
            error=error,
        )

    def execute_path(
        self,
        request: ExecutionPathRequest,
        graph_service
    ) -> ExecutionPathResponse:
        """Execute a specific path through the graph."""
        execution_id = str(uuid.uuid4())
        start_time = time.time()

        # Get the graph
        graph = graph_service.get_graph_instance(request.graph_id)
        if graph is None:
            raise ValueError(f"Graph not found: {request.graph_id}")

        # Execute each node in sequence
        steps = []
        current_state = request.initial_state.copy()
        status = "success"
        overall_error = None

        for node_id in request.node_ids:
            node = graph.nodes.get(node_id)
            if node is None:
                status = "error"
                overall_error = f"Node not found: {node_id}"
                break

            step_start = time.time()
            input_state = current_state.copy()
            step_status = "success"
            step_error = None

            try:
                if node.data is not None and callable(node.data):
                    output_state = node.execute(current_state)
                    current_state.update(output_state)
                else:
                    output_state = current_state.copy()
            except Exception as e:
                step_status = "error"
                step_error = str(e)
                output_state = current_state.copy()
                status = "error"

            step_duration = (time.time() - step_start) * 1000

            steps.append(
                NodeExecutionStep(
                    node_id=node_id,
                    node_name=node.name,
                    input_state=input_state,
                    output_state=output_state,
                    duration_ms=step_duration,
                    status=step_status,
                    error=step_error,
                )
            )

            if status == "error":
                break

        total_duration = (time.time() - start_time) * 1000

        # Store execution
        self.executions[execution_id] = {
            "execution_id": execution_id,
            "graph_id": request.graph_id,
            "execution_type": "path",
            "status": status,
            "initial_state": request.initial_state,
            "final_state": current_state,
            "steps": steps,
            "duration_ms": total_duration,
            "started_at": datetime.now(),
            "completed_at": datetime.now(),
            "success": status == "success",
            "error": overall_error,
        }

        # Update graph last executed
        graph_service.update_last_executed(request.graph_id)

        return ExecutionPathResponse(
            execution_id=execution_id,
            graph_id=request.graph_id,
            node_ids=request.node_ids,
            status=status,
            steps=steps,
            final_state=current_state,
            total_duration_ms=total_duration,
            started_at=self.executions[execution_id]["started_at"],
            completed_at=self.executions[execution_id]["completed_at"],
        )

    def execute_full_graph(
        self,
        graph_id: str,
        request: GraphExecuteRequest,
        graph_service
    ) -> GraphExecuteResponse:
        """Execute the entire graph."""
        execution_id = str(uuid.uuid4())
        start_time = time.time()

        # Get the graph
        graph = graph_service.get_graph_instance(graph_id)
        if graph is None:
            raise ValueError(f"Graph not found: {graph_id}")

        # Set initial state
        graph.state = request.initial_state.copy()

        # Execute all nodes
        execution_history = []
        status = "success"

        try:
            final_state = graph.run_all_nodes()
            execution_history.append({
                "message": "Graph executed successfully",
                "final_state": final_state,
            })
        except Exception as e:
            status = "error"
            final_state = graph.state
            execution_history.append({
                "error": str(e),
                "partial_state": final_state,
            })

        duration_ms = (time.time() - start_time) * 1000
        now = datetime.now()

        # Store execution
        self.executions[execution_id] = {
            "execution_id": execution_id,
            "graph_id": graph_id,
            "execution_type": "full",
            "status": status,
            "initial_state": request.initial_state,
            "final_state": final_state,
            "execution_history": execution_history,
            "duration_ms": duration_ms,
            "started_at": now,
            "completed_at": now,
            "success": status == "success",
        }

        # Update graph last executed
        graph_service.update_last_executed(graph_id)

        return GraphExecuteResponse(
            execution_id=execution_id,
            graph_id=graph_id,
            status=status,
            final_state=final_state,
            execution_history=execution_history,
            duration_ms=duration_ms,
            started_at=now,
            completed_at=now,
        )

    def get_execution_history(
        self,
        graph_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> ExecutionHistoryResponse:
        """Get execution history."""
        executions = list(self.executions.values())

        # Filter by graph_id if provided
        if graph_id:
            executions = [e for e in executions if e["graph_id"] == graph_id]

        # Sort by started_at descending
        executions.sort(key=lambda x: x["started_at"], reverse=True)

        # Paginate
        total = len(executions)
        start = (page - 1) * page_size
        end = start + page_size
        page_executions = executions[start:end]

        records = [
            ExecutionRecord(
                execution_id=e["execution_id"],
                graph_id=e["graph_id"],
                execution_type=e["execution_type"],
                status=e["status"],
                duration_ms=e["duration_ms"],
                started_at=e["started_at"],
                completed_at=e["completed_at"],
                success=e["success"],
                error=e.get("error"),
            )
            for e in page_executions
        ]

        return ExecutionHistoryResponse(
            executions=records,
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_execution_details(self, execution_id: str) -> Optional[ExecutionDetailsResponse]:
        """Get details of a specific execution."""
        if execution_id not in self.executions:
            return None

        e = self.executions[execution_id]

        # Get steps if available
        steps = e.get("steps", [])
        
        # Get logs
        logs = []
        if "logs" in e:
            logs = [{"message": log, "timestamp": e["started_at"]} for log in e["logs"]]

        return ExecutionDetailsResponse(
            execution_id=e["execution_id"],
            graph_id=e["graph_id"],
            execution_type=e["execution_type"],
            status=e["status"],
            initial_state=e.get("initial_state", e.get("input_state", {})),
            final_state=e.get("final_state", e.get("output_state", {})),
            steps=steps,
            logs=logs,
            duration_ms=e["duration_ms"],
            started_at=e["started_at"],
            completed_at=e["completed_at"],
            success=e["success"],
            error=e.get("error"),
        )

    def mock_state(self, request: MockStateRequest) -> MockStateResponse:
        """Mock state at a specific node."""
        if request.graph_id not in self.mocked_states:
            self.mocked_states[request.graph_id] = {}

        self.mocked_states[request.graph_id][request.node_id] = request.state

        return MockStateResponse(
            graph_id=request.graph_id,
            node_id=request.node_id,
            state=request.state,
            message=f"State mocked for node {request.node_id}",
        )


# Global instance
_execution_service = ExecutionService()


def get_execution_service() -> ExecutionService:
    """Get the global execution service instance."""
    return _execution_service

