#!/usr/bin/env python3
"""
Test script to verify API is working and can load graphs
"""

import requests
import json
import sys

API_URL = "http://localhost:8000"

def test_health():
    """Test API health endpoint"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✅ API is healthy:", response.json())
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")
        return False

def test_list_graphs():
    """Test listing graphs"""
    print("\n🔍 Testing list graphs endpoint...")
    try:
        response = requests.get(f"{API_URL}/api/graphs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total']} graph(s)")
            for graph in data['graphs']:
                print(f"   - {graph['name']} (ID: {graph['graph_id'][:8]}...)")
            return True
        else:
            print(f"❌ Failed to list graphs: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to list graphs: {e}")
        return False

def test_load_graph():
    """Test loading a graph from file"""
    print("\n🔍 Testing load graph from file...")
    try:
        payload = {
            "file_path": "../backend/graph_1.py",
            "graph_name": "Test Graph",
            "description": "Test graph loaded via API"
        }
        response = requests.post(
            f"{API_URL}/api/graphs/load",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"✅ Graph loaded successfully!")
            print(f"   Graph ID: {data['graph_id']}")
            print(f"   Name: {data['name']}")
            print(f"   Nodes: {len(data['structure']['nodes'])}")
            print(f"   Edges: {len(data['structure']['edges'])}")
            return data['graph_id']
        else:
            print(f"❌ Failed to load graph: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Failed to load graph: {e}")
        return None

def test_get_graph(graph_id):
    """Test getting a specific graph"""
    print(f"\n🔍 Testing get graph endpoint...")
    try:
        response = requests.get(f"{API_URL}/api/graphs/{graph_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved graph successfully!")
            print(f"   Name: {data['name']}")
            print(f"   Description: {data.get('description', 'N/A')}")
            print(f"   Nodes: {list(data['structure']['nodes'].keys())}")
            return True
        else:
            print(f"❌ Failed to get graph: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to get graph: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("API Connection Test Suite")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ API is not running or not accessible")
        print("   Start the API with: cd api && ./start_server.sh")
        sys.exit(1)
    
    # Test list graphs
    test_list_graphs()
    
    # Test load graph
    graph_id = test_load_graph()
    
    # Test get graph
    if graph_id:
        test_get_graph(graph_id)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\nThe frontend should now be able to connect to the API.")
    print("Start the frontend with: cd client && npm run dev")

if __name__ == "__main__":
    main()

