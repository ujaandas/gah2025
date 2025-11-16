"""
Testing nodes for LangGraph workflows.

This package provides testing nodes that can be integrated into LangGraph
workflows to automatically test for vulnerabilities and edge cases.
"""

from testing_nodes.fuzzer_node import FuzzerNode, create_fuzzer_node
from testing_nodes.prompt_injection_node import PromptInjectionNode, create_prompt_injection_node

__all__ = [
    'FuzzerNode',
    'create_fuzzer_node',
    'PromptInjectionNode',
    'create_prompt_injection_node'
]

__version__ = '1.0.0'

