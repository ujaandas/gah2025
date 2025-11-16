import type { Edge } from 'reactflow';

/**
 * Find all downstream nodes from a given node using BFS
 */
export function findDownstreamNodes(
  startNodeId: string,
  allEdges: Edge[]
): Set<string> {
  const downstream = new Set<string>();
  const queue = [startNodeId];
  const visited = new Set<string>();

  while (queue.length > 0) {
    const currentId = queue.shift()!;
    if (visited.has(currentId)) continue;
    visited.add(currentId);

    // Find all edges where current node is the source
    const outgoingEdges = allEdges.filter(e => e.source === currentId);
    
    for (const edge of outgoingEdges) {
      if (!visited.has(edge.target)) {
        downstream.add(edge.target);
        queue.push(edge.target);
      }
    }
  }

  return downstream;
}

/**
 * Find all upstream nodes from a given node using BFS
 */
export function findUpstreamNodes(
  startNodeId: string,
  allEdges: Edge[]
): Set<string> {
  const upstream = new Set<string>();
  const queue = [startNodeId];
  const visited = new Set<string>();

  while (queue.length > 0) {
    const currentId = queue.shift()!;
    if (visited.has(currentId)) continue;
    visited.add(currentId);

    // Find all edges where current node is the target
    const incomingEdges = allEdges.filter(e => e.target === currentId);
    
    for (const edge of incomingEdges) {
      if (!visited.has(edge.source)) {
        upstream.add(edge.source);
        queue.push(edge.source);
      }
    }
  }

  return upstream;
}

