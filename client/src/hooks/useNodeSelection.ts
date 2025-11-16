import { useState, useCallback } from 'react';
import type { Node, Edge } from 'reactflow';

/**
 * Hook to handle node selection and deletion
 */
export function useNodeSelection(
  edges: Edge[],
  setNodes: (callback: (nodes: Node[]) => Node[]) => void,
  setEdges: (callback: (edges: Edge[]) => Edge[]) => void
) {
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const onNodeClick = useCallback((_event: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  }, []);

  const handleDeleteNode = useCallback(() => {
    if (selectedNode && selectedNode.type === 'promptInject') {
      // Remove the node
      setNodes((nds) => nds.filter((n) => n.id !== selectedNode.id));
      
      // Find edges connected to this node
      const incomingEdge = edges.find(e => e.target === selectedNode.id);
      const outgoingEdge = edges.find(e => e.source === selectedNode.id);
      
      // If both edges exist, reconnect them
      if (incomingEdge && outgoingEdge) {
        setEdges((eds) => {
          // Remove edges connected to this node
          const filteredEdges = eds.filter(
            e => e.source !== selectedNode.id && e.target !== selectedNode.id
          );
          
          // Create new edge connecting the previous source to the next target
          const timestamp = Date.now();
          const reconnectEdge: Edge = {
            id: `e-${incomingEdge.source}-${outgoingEdge.target}-${timestamp}`,
            source: incomingEdge.source,
            target: outgoingEdge.target,
            animated: incomingEdge.animated || outgoingEdge.animated,
            style: incomingEdge.style || outgoingEdge.style,
          };
          
          return [...filteredEdges, reconnectEdge];
        });
      } else {
        // Just remove connected edges if not forming a bridge
        setEdges((eds) => eds.filter(
          e => e.source !== selectedNode.id && e.target !== selectedNode.id
        ));
      }
      
      setSelectedNode(null);
      console.log('Deleted node:', selectedNode.id);
    }
  }, [selectedNode, edges, setNodes, setEdges]);

  return {
    selectedNode,
    setSelectedNode,
    onNodeClick,
    handleDeleteNode
  };
}

