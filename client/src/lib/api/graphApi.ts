/**
 * API client for interacting with the LangGraph Testing Platform API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types matching the API models
export interface NodeInfo {
  id: string;
  name: string;
  node_type: string;
  is_testing: boolean;
  metadata: Record<string, any>;
}

export interface EdgeInfo {
  source: string;
  target: string;
  conditional: boolean;
  metadata: Record<string, any>;
}

export interface GraphStructure {
  nodes: Record<string, NodeInfo>;
  edges: EdgeInfo[];
  start_nodes: string[];
  end_nodes: string[];
}

export interface GraphLoadRequest {
  code?: string;
  file_path?: string;
  module_path?: string;
  graph_name: string;
  description?: string;
}

export interface GraphLoadResponse {
  graph_id: string;
  name: string;
  description?: string;
  structure: GraphStructure;
  created_at: string;
}

export interface GraphResponse {
  graph_id: string;
  name: string;
  description?: string;
  structure: GraphStructure;
  created_at: string;
  last_executed?: string;
}

export interface GraphListItem {
  graph_id: string;
  name: string;
  description?: string;
  node_count: number;
  edge_count: number;
  created_at: string;
  last_executed?: string;
}

export interface GraphListResponse {
  graphs: GraphListItem[];
  total: number;
}

export interface TestingNodeTemplate {
  node_type: string;
  display_name: string;
  description: string;
  icon: string;
  default_config: Record<string, any>;
  config_schema: Record<string, any>;
}

export interface TestingNodeAddRequest {
  graph_id: string;
  node_type: string;
  position: string;
  config?: Record<string, any>;
  name?: string;
}

export interface TestingNodeAddResponse {
  node_id: string;
  graph_id: string;
  node_type: string;
  position: string;
  config: Record<string, any>;
  message: string;
}

export interface GraphExecuteRequest {
  initial_state?: Record<string, any>;
  config?: Record<string, any>;
}

export interface StreamExecutionEvent {
  event_type: 'start' | 'node_start' | 'node_complete' | 'complete' | 'error';
  execution_id: string;
  graph_id: string;
  timestamp: string;
  node_id?: string;
  node_name?: string;
  status?: string;
  input_state?: Record<string, any>;
  output_state?: Record<string, any>;
  duration_ms?: number;
  error?: string;
  message?: string;
}

/**
 * Graph API Client
 */
export class GraphApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Load a graph from code, file, or module
   */
  async loadGraph(request: GraphLoadRequest): Promise<GraphLoadResponse> {
    const response = await fetch(`${this.baseUrl}/api/graphs/load`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `Failed to load graph: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * List all loaded graphs
   */
  async listGraphs(): Promise<GraphListResponse> {
    const response = await fetch(`${this.baseUrl}/api/graphs`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to list graphs: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get a specific graph by ID
   */
  async getGraph(graphId: string): Promise<GraphResponse> {
    const response = await fetch(`${this.baseUrl}/api/graphs/${graphId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `Failed to get graph: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Delete a graph
   */
  async deleteGraph(graphId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/graphs/${graphId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `Failed to delete graph: ${response.statusText}`);
    }
  }

  /**
   * Check if API is healthy
   */
  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${this.baseUrl}/health`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error('API health check failed');
    }

    return response.json();
  }

  /**
   * Get available testing node templates
   */
  async getTestingNodeTemplates(): Promise<TestingNodeTemplate[]> {
    const response = await fetch(`${this.baseUrl}/api/testing-nodes/templates`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get testing node templates: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Add a testing node to a graph
   */
  async addTestingNode(request: TestingNodeAddRequest): Promise<TestingNodeAddResponse> {
    const response = await fetch(`${this.baseUrl}/api/testing-nodes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `Failed to add testing node: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Execute a graph with streaming updates via Server-Sent Events
   */
  streamExecuteGraph(
    graphId: string,
    request: GraphExecuteRequest,
    onEvent: (event: StreamExecutionEvent) => void,
    onError?: (error: Error) => void,
    onComplete?: () => void
  ): () => void {
    const url = `${this.baseUrl}/api/graphs/${graphId}/execute/stream`;
    
    // Use fetch for SSE instead of EventSource (more control over request)
    const controller = new AbortController();
    
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    })
      .then(async (response) => {
        if (!response.ok) {
          const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
          throw new Error(error.detail || `Failed to execute graph: ${response.statusText}`);
        }

        if (!response.body) {
          throw new Error('Response body is null');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            if (onComplete) onComplete();
            break;
          }

          // Decode the chunk and add to buffer
          buffer += decoder.decode(value, { stream: true });

          // Process complete SSE messages
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = line.slice(6); // Remove 'data: ' prefix
                if (data.trim()) {
                  const event = JSON.parse(data) as StreamExecutionEvent;
                  onEvent(event);
                }
              } catch (e) {
                console.error('Failed to parse SSE event:', e, line);
              }
            }
          }
        }
      })
      .catch((error) => {
        if (error.name !== 'AbortError' && onError) {
          onError(error);
        }
      });

    // Return cleanup function
    return () => {
      controller.abort();
    };
  }
}

// Export singleton instance
export const graphApiClient = new GraphApiClient();

