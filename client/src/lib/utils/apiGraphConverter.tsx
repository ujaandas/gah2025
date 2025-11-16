/**
 * Convert API graph structure to React Flow format
 * This is separate from graphConverter.tsx to avoid duplication
 */

import type { Node, Edge } from 'reactflow';
import type { GraphStructure } from '../api/graphApi';

interface ReactFlowGraph {
  nodes: Node[];
  edges: Edge[];
}

/**
 * Convert API graph structure to React Flow nodes and edges
 */
export function convertApiGraphToReactFlow(graphStructure: GraphStructure): ReactFlowGraph {
  const nodes: Node[] = [];
  const edges: Edge[] = [];

  // Convert nodes
  Object.entries(graphStructure.nodes).forEach(([nodeId, nodeInfo], index) => {
    const icon = nodeInfo.metadata?.icon || '📦';
    const isStart = nodeInfo.node_type === 'start' || nodeId === '__start__';
    const isEnd = nodeInfo.node_type === 'end' || nodeId === '__end__';

    // Calculate position in a circular layout
    const totalNodes = Object.keys(graphStructure.nodes).length;
    const angle = (index / totalNodes) * 2 * Math.PI;
    const radius = 300;
    const centerX = 400;
    const centerY = 300;

    nodes.push({
      id: nodeId,
      type: 'default',
      position: {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      },
      data: {
        label: `${icon} ${nodeInfo.name}`,
        title: nodeInfo.name,
        icon: icon,
      },
      style: {
        background: isStart
          ? '#dcfce7'
          : isEnd
          ? '#fee2e2'
          : nodeInfo.is_testing
          ? '#fef3c7'
          : '#f3f4f6',
        border: '2px solid',
        borderColor: isStart
          ? '#22c55e'
          : isEnd
          ? '#ef4444'
          : nodeInfo.is_testing
          ? '#f59e0b'
          : '#9ca3af',
        padding: '10px',
        borderRadius: '8px',
        fontSize: '14px',
      },
    });
  });

  // Convert edges
  graphStructure.edges.forEach((edgeInfo, index) => {
    const edgeLabel = edgeInfo.metadata?.label || undefined;

    edges.push({
      id: `${edgeInfo.source}-${edgeInfo.target}-${index}`,
      source: edgeInfo.source,
      target: edgeInfo.target,
      type: edgeInfo.conditional ? 'smoothstep' : 'default',
      animated: false,
      label: edgeLabel,
      data: {
        conditional: edgeInfo.conditional,
      },
      style: {
        stroke: edgeInfo.conditional ? '#f59e0b' : '#9ca3af',
        strokeWidth: 2,
      },
      markerEnd: {
        type: 'arrowclosed',
        color: edgeInfo.conditional ? '#f59e0b' : '#9ca3af',
      },
    });
  });

  return { nodes, edges };
}

