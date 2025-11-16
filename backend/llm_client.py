"""
LLM Client for calling the team's LLM API.

This module provides a centralized client for interacting with the LLM API endpoint
that supports multiple models from Anthropic, Meta, Amazon Nova, Mistral, and DeepSeek.
"""

import os
import logging
import httpx
import json
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with the team's LLM API."""
    
    # API configuration
    API_ENDPOINT = "https://ctwa92wg1b.execute-api.us-east-1.amazonaws.com/prod/invoke"
    
    # Recommended models
    DEFAULT_MODEL = "us.deepseek.r1-v1:0"
    FAST_MODEL = "us.deepseek.r1-v1:0"
    POWERFUL_MODEL = "us.deepseek.r1-v1:0"
    
    def __init__(
        self,
        team_id: Optional[str] = None,
        api_token: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 120.0
    ):
        """
        Initialize the LLM client.
        
        Args:
            team_id: Team ID for authentication. If None, reads from TEAM_ID env var.
            api_token: API token for authentication. If None, reads from API_TOKEN env var.
            model: Model to use. If None, uses DEFAULT_MODEL.
            timeout: Request timeout in seconds.
        """
        self.team_id = team_id or os.getenv("TEAM_ID")
        self.api_token = api_token or os.getenv("API_TOKEN")
        self.model = model or self.DEFAULT_MODEL
        self.timeout = timeout
        
        if not self.team_id:
            raise ValueError("TEAM_ID must be provided or set in environment variables")
        if not self.api_token:
            raise ValueError("API_TOKEN must be provided or set in environment variables")
        
        logger.info(f"LLM Client initialized with model: {self.model}")
    
    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> str:
        """
        Make a simple call to the LLM API.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation (0.0 to 1.0)
            model: Optional model override
            
        Returns:
            The generated text response
            
        Raises:
            httpx.HTTPError: If the API call fails
            ValueError: If the response format is unexpected
        """
        messages = []
        
        # Add system message if provided
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add user message
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        return self.call_with_messages(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            model=model
        )
    
    def call_with_messages(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9,
        model: Optional[str] = None
    ) -> str:
        """
        Make a call to the LLM API with a full message history.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            top_p: Top-p sampling parameter
            model: Optional model override
            
        Returns:
            The generated text response
            
        Raises:
            httpx.HTTPError: If the API call fails
            ValueError: If the response format is unexpected
        """
        use_model = model or self.model
        
        headers = {
            "Content-Type": "application/json",
            "X-Team-ID": self.team_id,
            "X-API-Token": self.api_token
        }
        
        # Filter out system messages and convert them to user message prefix
        # The API only supports 'user' and 'assistant' roles
        filtered_messages = []
        system_prefix = ""
        
        for msg in messages:
            if msg.get("role") == "system":
                # Convert system message to a prefix for the first user message
                system_prefix += msg.get("content", "") + "\n\n"
            else:
                filtered_messages.append(msg)
        
        # If we have a system prefix, add it to the first user message
        if system_prefix and filtered_messages:
            for i, msg in enumerate(filtered_messages):
                if msg.get("role") == "user":
                    filtered_messages[i] = {
                        "role": "user",
                        "content": system_prefix + msg.get("content", "")
                    }
                    break
        
        payload = {
            "team_id": self.team_id,
            "model": use_model,
            "messages": filtered_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
        
        logger.debug(f"Calling LLM API with model: {use_model}")
        logger.debug(f"Messages: {len(filtered_messages)} filtered messages")
        logger.debug(f"Payload: {payload}")
        
        try:
            # WORKAROUND: Use curl via subprocess since Python HTTP libraries fail with this API
            # This is a known issue with some AWS API Gateways that have strict request validation
            curl_command = [
                'curl', '-s', '-X', 'POST', self.API_ENDPOINT,
                '-H', 'Content-Type: application/json',
                '-H', f'X-Team-ID: {self.team_id}',
                '-H', f'X-API-Token: {self.api_token}',
                '-d', json.dumps(payload)
            ]
            
            result_process = subprocess.run(
                curl_command,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result_process.returncode != 0:
                error_msg = f"curl command failed with code {result_process.returncode}: {result_process.stderr}"
                logger.error(error_msg)
                logger.error(f"stdout: {result_process.stdout}")
                raise httpx.HTTPError(error_msg)
            
            # Check if response contains an error
            if "error" in result_process.stdout.lower() or result_process.stdout.strip().startswith("{\"error\""):
                logger.error(f"API returned error: {result_process.stdout}")
                # Parse to get the actual error
                try:
                    error_data = json.loads(result_process.stdout)
                    raise ValueError(f"API Error: {error_data.get('error', result_process.stdout)}")
                except:
                    raise ValueError(f"API Error: {result_process.stdout}")
            
            try:
                result = json.loads(result_process.stdout)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse API response: {result_process.stdout}")
                raise ValueError(f"Invalid JSON response: {e}")
            
            # Extract text from response
            # Expected format: {"content": [{"text": "..."}]}
            if "content" in result and isinstance(result["content"], list):
                if len(result["content"]) > 0 and "text" in result["content"][0]:
                    text = result["content"][0]["text"]
                    logger.debug(f"Received response: {len(text)} characters")
                    return text
            
            # Fallback: try to extract text from different formats
            if "text" in result:
                return result["text"]
            if "response" in result:
                return result["response"]
            
            raise ValueError(f"Unexpected response format: {result}")
        
        except subprocess.TimeoutExpired:
            logger.error("LLM API call timed out")
            raise httpx.TimeoutException("LLM API call timed out")
        except Exception as e:
            logger.error(f"Unexpected error calling LLM API: {str(e)}")
            raise
    
    def call_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        tool_choice: str = "auto",
        max_tokens: int = 1024,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make a call to the LLM API with tool/function calling support.
        
        Note: Tool calling is natively supported by Claude, DeepSeek, and Amazon Nova models.
        Llama and Mistral models may not support this at the API level.
        
        Args:
            prompt: The user prompt
            tools: List of tool definitions
            tool_choice: "auto", "any", or {"name": "tool_name"}
            max_tokens: Maximum tokens to generate
            model: Optional model override
            
        Returns:
            The full API response including any tool calls
        """
        use_model = model or self.model
        
        headers = {
            "Content-Type": "application/json",
            "X-Team-ID": self.team_id,
            "X-API-Token": self.api_token
        }
        
        payload = {
            "team_id": self.team_id,
            "model": use_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "tools": tools,
            "tool_choice": tool_choice,
            "max_tokens": max_tokens
        }
        
        logger.debug(f"Calling LLM API with tools: {len(tools)} tools")
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.API_ENDPOINT,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling LLM API with tools: {str(e)}")
            raise


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client(
    team_id: Optional[str] = None,
    api_token: Optional[str] = None,
    model: Optional[str] = None,
    force_new: bool = False
) -> LLMClient:
    """
    Get or create the global LLM client instance.
    
    Args:
        team_id: Team ID (optional, uses env var if not provided)
        api_token: API token (optional, uses env var if not provided)
        model: Model to use (optional)
        force_new: If True, creates a new instance
        
    Returns:
        LLMClient instance
    """
    global _llm_client
    
    if force_new or _llm_client is None:
        _llm_client = LLMClient(
            team_id=team_id,
            api_token=api_token,
            model=model
        )
    
    return _llm_client


# Convenience functions
def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    model: Optional[str] = None
) -> str:
    """
    Convenience function to call the LLM API.
    
    Args:
        prompt: The user prompt
        system_prompt: Optional system prompt
        max_tokens: Maximum tokens to generate
        temperature: Temperature for generation
        model: Optional model to use
        
    Returns:
        The generated text
    """
    client = get_llm_client()
    return client.call(
        prompt=prompt,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    )

