import { useState, useCallback, useEffect } from 'react';
import type { Node, Edge } from 'reactflow';
import { distanceToLineSegment, isVerticalEdge, getMidpoint } from '@/lib/utils/geometry';
import { findDownstreamNodes, findUpstreamNodes } from '@/lib/utils/graphTraversal';

/**
 * Hook to handle drag and drop of nodes onto edges
 */
export function useNodeDragAndDrop(
  nodes: Node[],
  edges: Edge[],
  initialEdges: Edge[],
  setNodes: (callback: (nodes: Node[]) => Node[]) => void,
  setEdges: (callback: (edges: Edge[]) => Edge[]) => void,
  fitView: (options?: any) => void
) {
  const [draggedNode, setDraggedNode] = useState<Node | null>(null);
  const [hoveredEdge, setHoveredEdge] = useState<string | null>(null);

  const onNodeDragStart = useCallback((_event: React.MouseEvent, node: Node) => {
    if (node.type === 'promptInject') {
      // Check if the node is already part of the graph
      const hasIncomingEdge = edges.some(e => e.target === node.id);
      const hasOutgoingEdge = edges.some(e => e.source === node.id);
      
      // Only allow dragging if not connected
      if (!hasIncomingEdge || !hasOutgoingEdge) {
        setDraggedNode(node);
      }
    }
  }, [edges]);

  const onNodeDrag = useCallback((_event: React.MouseEvent, node: Node) => {
    if (node.type !== 'promptInject') return;

    // Check if node is already part of the graph
    const hasIncomingEdge = edges.some(e => e.target === node.id);
    const hasOutgoingEdge = edges.some(e => e.source === node.id);
    
    if (hasIncomingEdge && hasOutgoingEdge) {
      return; // Node is locked
    }

    // Get the position of the dragged node
    const nodeCenter = {
      x: node.position.x + 50,
      y: node.position.y + 25
    };

    // Check if the node is over any edge
    let foundEdge: string | null = null;
    
    for (const edge of edges) {
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

  const onNodeDragStop = useCallback((_event: React.MouseEvent, node: Node) => {
    if (node.type !== 'promptInject' || !hoveredEdge) {
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
          draggable: false
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

    // Fit view with animation
    setTimeout(() => {
      fitView({ 
        duration: 400,
        padding: 0.2,
      });
    }, 50);

    setDraggedNode(null);
    setHoveredEdge(null);
  }, [hoveredEdge, nodes, edges, setNodes, setEdges, fitView]);

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

