"""Test script for streaming execution endpoint."""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"


def test_streaming_execution():
    """Test the streaming execution endpoint."""
    
    print("=" * 60)
    print("Testing Streaming Execution Endpoint")
    print("=" * 60)
    
    # First, load a graph
    print("\n1. Loading graph from backend/graph_2.py...")
    load_response = requests.post(
        f"{API_BASE_URL}/api/graphs/load",
        json={
            "file_path": "../backend/graph_2.py",
            "graph_name": "Test Graph",
            "description": "Testing streaming execution"
        }
    )
    
    if load_response.status_code != 201:
        print(f"❌ Failed to load graph: {load_response.status_code}")
        print(load_response.text)
        return False
    
    graph_data = load_response.json()
    graph_id = graph_data["graph_id"]
    print(f"✓ Graph loaded successfully: {graph_id}")
    print(f"  - Name: {graph_data['name']}")
    print(f"  - Nodes: {len(graph_data['structure']['nodes'])}")
    print(f"  - Edges: {len(graph_data['structure']['edges'])}")
    
    # Now test streaming execution
    print(f"\n2. Starting streaming execution for graph {graph_id}...")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/graphs/{graph_id}/execute/stream",
            json={"initial_state": {}},
            stream=True,
            headers={"Accept": "text/event-stream"}
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to start execution: {response.status_code}")
            print(response.text)
            return False
        
        event_count = 0
        node_events = []
        
        # Process the stream
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    event_count += 1
                    data_str = line_str[6:]  # Remove 'data: ' prefix
                    event = json.loads(data_str)
                    
                    event_type = event.get('event_type')
                    
                    if event_type == 'start':
                        print(f"\n🚀 {event.get('message', 'Execution started')}")
                        print(f"   Execution ID: {event.get('execution_id')}")
                    
                    elif event_type == 'node_start':
                        node_name = event.get('node_name', event.get('node_id', 'Unknown'))
                        print(f"\n▶️  Node: {node_name}")
                        print(f"   Status: Starting...")
                    
                    elif event_type == 'node_complete':
                        node_name = event.get('node_name', event.get('node_id', 'Unknown'))
                        status = event.get('status', 'unknown')
                        duration = event.get('duration_ms', 0)
                        
                        status_icon = "✓" if status == "success" else "✗"
                        print(f"   {status_icon} Status: {status}")
                        print(f"   Duration: {duration:.2f}ms")
                        
                        if event.get('error'):
                            print(f"   Error: {event['error']}")
                        
                        node_events.append({
                            'node': node_name,
                            'status': status,
                            'duration': duration
                        })
                    
                    elif event_type == 'complete':
                        total_duration = event.get('duration_ms', 0)
                        print(f"\n✅ {event.get('message', 'Execution completed')}")
                        print(f"   Total Duration: {total_duration:.2f}ms")
                    
                    elif event_type == 'error':
                        print(f"\n❌ Error: {event.get('message', 'Unknown error')}")
                        if event.get('error'):
                            print(f"   Details: {event['error']}")
        
        print("\n" + "-" * 60)
        print(f"Stream completed: {event_count} events received")
        
        # Summary
        print("\n3. Execution Summary:")
        print(f"   - Total Events: {event_count}")
        print(f"   - Nodes Executed: {len(node_events)}")
        
        if node_events:
            success_count = sum(1 for n in node_events if n['status'] == 'success')
            error_count = sum(1 for n in node_events if n['status'] == 'error')
            total_time = sum(n['duration'] for n in node_events)
            
            print(f"   - Successful: {success_count}")
            print(f"   - Failed: {error_count}")
            print(f"   - Total Time: {total_time:.2f}ms")
        
        print("\n✓ Streaming execution test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during streaming: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        # Check if server is running
        try:
            health = requests.get(f"{API_BASE_URL}/health", timeout=2)
            if health.status_code != 200:
                print("❌ API server is not healthy")
                sys.exit(1)
        except requests.exceptions.RequestException:
            print("❌ Cannot connect to API server at", API_BASE_URL)
            print("   Please start the server with: cd api && ./start_server.sh")
            sys.exit(1)
        
        # Run the test
        success = test_streaming_execution()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)

