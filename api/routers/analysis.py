"""Analysis and reporting endpoints."""

from fastapi import APIRouter, HTTPException, status, Query, Response
from typing import Optional

from models.analysis import (
    TestSuiteRequest,
    TestSuiteResponse,
    VulnerabilityReport,
    ExportFormat,
    LLMAnalysisRequest,
    LLMAnalysisResponse,
)
from services.analysis_service import get_analysis_service
from services.execution_service import get_execution_service
from services.graph_service import get_graph_service

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/test-suite", response_model=TestSuiteResponse)
async def run_test_suite(request: TestSuiteRequest):
    """
    Run a test suite with multiple test cases.
    
    Executes a series of test cases against the graph and returns
    comprehensive results including:
    - Pass/fail status for each test
    - Vulnerabilities discovered
    - Performance metrics
    """
    try:
        analysis_service = get_analysis_service()
        execution_service = get_execution_service()
        graph_service = get_graph_service()
        
        response = analysis_service.run_test_suite(
            request,
            execution_service,
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
            detail=f"Failed to run test suite: {str(e)}"
        )


@router.get("/vulnerabilities/{graph_id}", response_model=VulnerabilityReport)
async def get_vulnerability_report(graph_id: str):
    """
    Get vulnerability report for a graph.
    
    Returns a comprehensive report of all vulnerabilities found during
    testing, categorized by severity and type, with recommendations
    for remediation.
    """
    analysis_service = get_analysis_service()
    
    report = analysis_service.get_vulnerability_report(graph_id)
    if report is None:
        # Return empty report if no tests have been run
        return VulnerabilityReport(
            graph_id=graph_id,
            total_vulnerabilities=0,
            by_severity={},
            by_type={},
            vulnerabilities=[],
            recommendations=[],
        )
    
    return report


@router.get("/export/{graph_id}")
async def export_results(
    graph_id: str,
    format: ExportFormat = Query(ExportFormat.JSON, description="Export format")
):
    """
    Export test results and vulnerability reports.
    
    Supported formats:
    - json: JSON format for programmatic access
    - csv: CSV format for spreadsheet analysis
    - pdf: PDF report (coming soon)
    - html: HTML report for viewing in browser
    """
    try:
        analysis_service = get_analysis_service()
        execution_service = get_execution_service()
        graph_service = get_graph_service()
        
        data = analysis_service.export_results(
            graph_id,
            format,
            graph_service,
            execution_service
        )
        
        # Set appropriate content type
        content_types = {
            ExportFormat.JSON: "application/json",
            ExportFormat.CSV: "text/csv",
            ExportFormat.PDF: "application/pdf",
            ExportFormat.HTML: "text/html",
        }
        
        return Response(
            content=data,
            media_type=content_types[format],
            headers={
                "Content-Disposition": f"attachment; filename=report-{graph_id}.{format.value}"
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export results: {str(e)}"
        )


@router.post("/llm-analysis", response_model=LLMAnalysisResponse)
async def generate_llm_analysis(request: LLMAnalysisRequest):
    """
    Generate LLM-powered analysis of execution results.
    
    This endpoint uses an AI model to analyze the execution of a graph and provide:
    - Summary of what happened
    - Detected vulnerabilities and security issues
    - Recommendations for improvement
    - Detailed analysis
    - Risk score (0-100)
    """
    try:
        analysis_service = get_analysis_service()
        execution_service = get_execution_service()
        graph_service = get_graph_service()
        
        response = analysis_service.generate_llm_analysis(
            request,
            execution_service,
            graph_service
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate LLM analysis: {str(e)}"
        )


@router.get("/llm-analysis/{analysis_id}", response_model=LLMAnalysisResponse)
async def get_llm_analysis(analysis_id: str):
    """
    Retrieve a previously generated LLM analysis.
    """
    analysis_service = get_analysis_service()
    analysis = analysis_service.get_llm_analysis(analysis_id)
    
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis not found: {analysis_id}"
        )
    
    return analysis

