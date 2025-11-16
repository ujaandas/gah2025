import { useState, useCallback, useEffect } from 'react';
import type { Node, Edge } from 'reactflow';
import { distanceToLineSegment, isVerticalEdge, getMidpoint } from '@/lib/utils/geometry';
import { findDownstreamNodes, findUpstreamNodes } from '@/lib/utils/graphTraversal';
import { graphApiClient } from '@/lib/api/graphApi';

/**
 * Hook to handle drag and drop of nodes onto edges
 */
export function useNodeDragAndDrop(
  nodes: Node[],
  edges: Edge[],
  initialEdges: Edge[],
  setNodes: (callback: (nodes: Node[]) => Node[]) => void,
  setEdges: (callback: (edges: Edge[]) => Edge[]) => void,
  fitView: (options?: any) => void,
  graphId: string | null,
  addLog?: (log: { level: 'info' | 'warning' | 'error' | 'success'; message: string; source?: string }) => void
) {
  const [draggedNode, setDraggedNode] = useState<Node | null>(null);
  const [hoveredEdge, setHoveredEdge] = useState<string | null>(null);

  const onNodeDragStart = useCallback((_event: React.MouseEvent, node: Node) => {
    if (node.type === 'promptInject') {
      setDraggedNode(node);
    }
  }, []);

  const onNodeDrag = useCallback((_event: React.MouseEvent, node: Node) => {
    if (node.type !== 'promptInject') return;

    // Check if node is already part of the graph
    const hasIncomingEdge = edges.some(e => e.target === node.id);
    const hasOutgoingEdge = edges.some(e => e.source === node.id);
    
    // If node is already connected, don't allow dropping on edges
    if (hasIncomingEdge && hasOutgoingEdge) {
      setHoveredEdge(null);
      return;
    }

    // Get the position of the dragged node
    const nodeCenter = {
      x: node.position.x + 50,
      y: node.position.y + 25
    };

    // Check if the node is over any edge (excluding edges connected to this node)
    let foundEdge: string | null = null;
    
    for (const edge of edges) {
      // Skip edges that are already connected to this node
      if (edge.source === node.id || edge.target === node.id) continue;
      
      const sourceNode = nodes.find(n => n.id === edge.source);
      const targetNode = nodes.find(n => n.id === edge.target);
      
      if (!sourceNode || !targetNode) continue;

      // Calculate distance from node center to edge line
      const distance = distanceToLineSegment(
        nodeCenter,
        { x: sourceNode.position.x + 50, y: sourceNode.position.y + 25 },
        { x: targetNode.position.x + 50, y: targetNode.position.y + 25 }
      );

      // If within 30 pixels of the edge, consider it hovering
      if (distance < 30) {
        foundEdge = edge.id;
        break;
      }
    }

    setHoveredEdge(foundEdge);
  }, [nodes, edges]);

  const onNodeDragStop = useCallback(async (_event: React.MouseEvent, node: Node) => {
    if (node.type !== 'promptInject' || !hoveredEdge) {
      setDraggedNode(null);
      setHoveredEdge(null);
      return;
    }

    // Check if node is already part of the graph
    const hasIncomingEdge = edges.some(e => e.target === node.id);
    const hasOutgoingEdge = edges.some(e => e.source === node.id);
    
    // If node is already connected, don't allow dropping on edges
    if (hasIncomingEdge && hasOutgoingEdge) {
      setDraggedNode(null);
      setHoveredEdge(null);
      return;
    }

    // Find the edge that was hovered
    const edge = edges.find(e => e.id === hoveredEdge);
    if (!edge) {
      setDraggedNode(null);
      setHoveredEdge(null);
      return;
    }

    // Prevent self-loops
    if (edge.source === node.id || edge.target === node.id) {
      setDraggedNode(null);
      setHoveredEdge(null);
      return;
    }

    // Get source and target nodes
    const sourceNode = nodes.find(n => n.id === edge.source);
    const targetNode = nodes.find(n => n.id === edge.target);

    if (!sourceNode || !targetNode) {
      setDraggedNode(null);
      setHoveredEdge(null);
      return;
    }

    // Calculate positioning
    const isVertical = isVerticalEdge(sourceNode.position, targetNode.position);
    const spacingAmount = 75;
    const newPosition = getMidpoint(sourceNode.position, targetNode.position);

    // Find nodes to push
    const upstreamNodes = findUpstreamNodes(edge.source, edges);
    upstreamNodes.add(edge.source);

    const downstreamNodes = findDownstreamNodes(edge.target, edges);
    downstreamNodes.add(edge.target);

    // Update positions
    setNodes((nds) => nds.map(n => {
      if (n.id === node.id) {
        return { 
          ...n, 
          position: newPosition,
          draggable: true
        };
      } else if (upstreamNodes.has(n.id)) {
        if (isVertical) {
          return {
            ...n,
            position: {
              x: n.position.x,
              y: n.position.y - spacingAmount
            }
          };
        } else {
          return {
            ...n,
            position: {
              x: n.position.x - spacingAmount,
              y: n.position.y
            }
          };
        }
      } else if (downstreamNodes.has(n.id)) {
        if (isVertical) {
          return {
            ...n,
            position: {
              x: n.position.x,
              y: n.position.y + spacingAmount
            }
          };
        } else {
          return {
            ...n,
            position: {
              x: n.position.x + spacingAmount,
              y: n.position.y
            }
          };
        }
      }
      return n;
    }));

    // Split the edge
    setEdges((eds) => {
      const filteredEdges = eds.filter(e => e.id !== edge.id);
      
      const timestamp = Date.now();
      const newEdge1: Edge = {
        id: `e-${edge.source}-${node.id}-${timestamp}-1`,
        source: edge.source,
        target: node.id,
        animated: false,
        style: { stroke: '#6b7280', strokeWidth: 2 },
      };

      const newEdge2: Edge = {
        id: `e-${node.id}-${edge.target}-${timestamp}-2`,
        source: node.id,
        target: edge.target,
        animated: false,
        style: { stroke: '#6b7280', strokeWidth: 2 },
      };

      return [...filteredEdges, newEdge1, newEdge2];
    });

    // Send API request to update the graph backend
    if (graphId && node.data.nodeType) {
      try {
        const position = `after:${edge.source}`;
        const nodeType = node.data.nodeType;
        
        if (addLog) {
          addLog({
            level: 'info',
            message: `Adding testing node ${node.id} to graph...`,
            source: 'API'
          });
        }
        
        const response = await graphApiClient.addTestingNode({
          graph_id: graphId,
          node_type: nodeType,
          position: position,
          name: node.id,
          config: node.data.config || {}
        });
        
        if (addLog) {
          addLog({
            level: 'success',
            message: `Testing node added to backend: ${response.message}`,
            source: 'API'
          });
        }
        
        console.log('Testing node added to backend:', response);
      } catch (error) {
        console.error('Failed to add testing node to backend:', error);
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        
        if (addLog) {
          if (errorMessage.includes('Graph not found')) {
            addLog({
              level: 'error',
              message: `Graph not found in API. Please reload the page to get a fresh graph.`,
              source: 'API'
            });
          } else {
            addLog({
              level: 'error',
              message: `Failed to add testing node: ${errorMessage}`,
              source: 'API'
            });
          }
        }
      }
    } else {
      console.warn('Cannot add testing node to backend: missing graphId or nodeType');
      if (addLog && !graphId) {
        addLog({
          level: 'warning',
          message: 'No graph loaded from API. Testing node added to UI only - please reload the page.',
          source: 'API'
        });
      }
    }

    // Fit view with animation
    setTimeout(() => {
      fitView({ 
        duration: 400,
        padding: 0.2,
      });
    }, 50);

    setDraggedNode(null);
    setHoveredEdge(null);
  }, [hoveredEdge, nodes, edges, setNodes, setEdges, fitView, graphId, addLog]);

  // Update edges to highlight when hovered
  useEffect(() => {
    if (hoveredEdge) {
      setEdges((eds) => eds.map(e => {
        if (e.id === hoveredEdge) {
          return {
            ...e,
            style: { ...e.style, stroke: '#3b82f6', strokeWidth: 4 },
            animated: true,
          };
        }
        const originalEdge = initialEdges.find(ie => 
          ie.source === e.source && ie.target === e.target
        );
        const strokeColor = originalEdge?.style?.stroke || '#6b7280';
        return {
          ...e,
          style: { stroke: strokeColor, strokeWidth: 2 },
          animated: false,
        };
      }));
    } else if (draggedNode) {
      setEdges((eds) => eds.map(e => {
        const originalEdge = initialEdges.find(ie => 
          ie.source === e.source && ie.target === e.target
        );
        const strokeColor = originalEdge?.style?.stroke || '#6b7280';
        return {
          ...e,
          style: { stroke: strokeColor, strokeWidth: 2 },
          animated: false,
        };
      }));
    }
  }, [hoveredEdge, draggedNode, setEdges, initialEdges]);

  return {
    draggedNode,
    hoveredEdge,
    onNodeDragStart,
    onNodeDrag,
    onNodeDragStop
  };
}

