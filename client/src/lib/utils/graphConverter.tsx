import type { Node, Edge } from 'reactflow';
import type { GraphStructure } from '../data/mockGraphData';

/**
 * Convert graph structure to React Flow nodes and edges
 */
export function convertGraphStructure(graphStructure: GraphStructure) {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  
  // Simple layout algorithm - arrange nodes in layers
  const layers: { [key: string]: string[] } = {
    start: [],
    middle: [],
    agents: [],
    end: []
  };

  // Categorize nodes
  Object.values(graphStructure.nodes).forEach(node => {
    if (node.node_type === 'start') {
      layers.start.push(node.id);
    } else if (node.node_type === 'end') {
      layers.end.push(node.id);
    } else if (node.id === 'supervisor') {
      layers.middle.push(node.id);
    } else {
      layers.agents.push(node.id);
    }
  });

  // Calculate positions
  const layerY = { start: 50, middle: 200, agents: 400, end: 600 };
  const centerX = 400;

  // Position nodes
  Object.values(graphStructure.nodes).forEach(node => {
    let position = { x: centerX, y: 300 };
    let nodeStyle = {};
    let reactFlowType: 'input' | 'output' | 'default' = 'default';

    if (node.node_type === 'start') {
      position = { x: centerX, y: layerY.start };
      reactFlowType = 'input';
      nodeStyle = {
        background: '#f9fafb',
        border: '2px solid #1f2937',
        borderRadius: '8px',
        padding: '10px'
      };
    } else if (node.node_type === 'end') {
      position = { x: centerX, y: layerY.end };
      reactFlowType = 'output';
      nodeStyle = {
        background: '#f9fafb',
        border: '2px solid #1f2937',
        borderRadius: '8px',
        padding: '10px'
      };
    } else if (node.id === 'supervisor') {
      position = { x: centerX - 50, y: layerY.middle };
      nodeStyle = {
        background: '#ffffff',
        border: '3px solid #1f2937',
        borderRadius: '12px',
        padding: '15px',
        minWidth: '150px'
      };
    } else {
      // Agent nodes - distribute horizontally
      const agentIndex = layers.agents.indexOf(node.id);
      const totalAgents = layers.agents.length;
      const spacing = 200;
      const startX = centerX - ((totalAgents - 1) * spacing) / 2;
      position = { x: startX + agentIndex * spacing, y: layerY.agents };
      nodeStyle = {
        background: '#f9fafb',
        border: '2px solid #4b5563',
        borderRadius: '8px',
        padding: '12px'
      };
    }

    const icon = node.metadata.icon || '⚙️';
    const description = (node.metadata as any).description;

    nodes.push({
      id: node.id,
      type: reactFlowType,
      position,
      data: {
        label: (
          <div className="flex flex-col items-center gap-1">
            <span className="text-2xl">{icon}</span>
            <span className={node.id === 'supervisor' ? 'font-bold' : 'font-semibold'}>{node.name}</span>
            {description && <span className="text-xs text-gray-500">{description}</span>}
          </div>
        )
      },
      style: nodeStyle
    });
  });

  // Convert edges
  graphStructure.edges.forEach((edge, index) => {
    const edgeStyle = edge.conditional 
      ? { stroke: '#1f2937', strokeWidth: 2 }
      : { stroke: '#6b7280', strokeWidth: 2 };

    edges.push({
      id: `e-${edge.source}-${edge.target}-${index}`,
      source: edge.source,
      target: edge.target,
      animated: false,
      style: edgeStyle,
      label: edge.metadata.label || undefined,
      data: { 
        conditional: edge.conditional 
      }
    });
  });

  return { nodes, edges };
}

