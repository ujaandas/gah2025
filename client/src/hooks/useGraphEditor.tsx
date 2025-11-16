import { useState, useCallback } from 'react';
import type { Node, Edge } from 'reactflow';

export interface ExecutionLog {
  id: string;
  timestamp: Date;
  level: 'info' | 'warning' | 'error' | 'success';
  message: string;
  source?: string;
}

/**
 * Hook to manage graph editor state and operations
 */
export function useGraphEditor() {
  const [isDirectoryOpen, setIsDirectoryOpen] = useState(false);
  const [isLogPanelOpen, setIsLogPanelOpen] = useState(false);
  const [nodeCounter, setNodeCounter] = useState<Record<string, number>>({});
  const [executionLogs, setExecutionLogs] = useState<ExecutionLog[]>([]);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executingNodeIds, setExecutingNodeIds] = useState<string[]>([]);

  // Add a log entry
  const addLog = useCallback((log: Omit<ExecutionLog, 'id' | 'timestamp'>) => {
    const newLog: ExecutionLog = {
      ...log,
      id: Date.now().toString() + Math.random().toString(36).substring(7),
      timestamp: new Date(),
    };
    setExecutionLogs((prev) => [newLog, ...prev].slice(0, 100)); // Keep last 100 logs
  }, []);

  // Clear logs
  const clearLogs = useCallback(() => {
    setExecutionLogs([]);
  }, []);

  // Execution layers for supervisor pattern
  const getSupervisorExecutionLayers = useCallback((
    nodes: Node[], 
    edges: Edge[], 
    startNode: Node, 
    supervisorNode: Node,
    addLog: (log: { level: string; message: string; source?: string }) => void
  ): string[][] => {
    const layers: string[][] = [];
    const endNode = nodes.find(n => n.id === '__end__');
    
    // Layer 1: Start node
    layers.push([startNode.id]);
    
    // Layer 2: Find nodes connected to start (typically supervisor)
    const fromStart = edges
      .filter(e => e.source === startNode.id)
      .map(e => e.target);
    if (fromStart.length > 0) {
      layers.push(fromStart);
    }
    
    // Layer 3: Find all agent nodes (nodes with conditional edges from supervisor)
    const agentNodes = edges
      .filter(e => {
        const isConditional = e.conditional || e.data?.conditional;
        return e.source === 'supervisor' && isConditional && e.target !== '__end__';
      })
      .map(e => e.target);
    
    if (agentNodes.length > 0) {
      layers.push(agentNodes); // Agents run concurrently
      
      // Layer 4: Supervisor again (to collect results)
      layers.push(['supervisor']);
    }
    
    // Layer 5: End node
    if (endNode) {
      layers.push([endNode.id]);
    }

    console.log('[getSupervisorExecutionLayers] Execution layers:', layers);
    return layers;
  }, []);

  // Execution layers for sequential/DAG graphs using topological sort
  const getTopologicalExecutionLayers = useCallback((
    nodes: Node[], 
    edges: Edge[], 
    startNode: Node,
    addLog: (log: { level: string; message: string; source?: string }) => void
  ): string[][] => {
    const layers: string[][] = [];
    const nodeIds = new Set(nodes.map(n => n.id));
    const visited = new Set<string>();
    const inDegree = new Map<string, number>();
    
    // Calculate in-degree for each node
    nodeIds.forEach(id => inDegree.set(id, 0));
    edges.forEach(edge => {
      if (nodeIds.has(edge.target)) {
        inDegree.set(edge.target, (inDegree.get(edge.target) || 0) + 1);
      }
    });
    
    console.log('[getTopologicalExecutionLayers] In-degrees:', Object.fromEntries(inDegree));
    
    // Process nodes layer by layer
    let currentLayer = [startNode.id];
    
    while (currentLayer.length > 0) {
      layers.push([...currentLayer]);
      currentLayer.forEach(nodeId => visited.add(nodeId));
      
      // Find next layer: nodes whose all predecessors have been visited
      const nextLayer = new Set<string>();
      
      currentLayer.forEach(nodeId => {
        // Find all nodes that this node connects to
        const outgoingEdges = edges.filter(e => e.source === nodeId);
        outgoingEdges.forEach(edge => {
          const targetId = edge.target;
          if (!visited.has(targetId) && nodeIds.has(targetId)) {
            // Check if all predecessors of targetId have been visited
            const predecessors = edges.filter(e => e.target === targetId);
            const allPredecessorsVisited = predecessors.every(e => visited.has(e.source));
            
            if (allPredecessorsVisited) {
              nextLayer.add(targetId);
            }
          }
        });
      });
      
      currentLayer = Array.from(nextLayer);
    }
    
    // Check if all nodes were visited
    if (visited.size < nodeIds.size) {
      const unvisited = Array.from(nodeIds).filter(id => !visited.has(id));
      console.warn('[getTopologicalExecutionLayers] Some nodes were not reached:', unvisited);
      addLog({ 
        level: 'warning', 
        message: `Some nodes are not connected to the start node: ${unvisited.join(', ')}`, 
        source: 'system' 
      });
    }
    
    console.log('[getTopologicalExecutionLayers] Execution layers:', layers);
    return layers;
  }, []);

  // Find execution layers - groups of nodes that can run concurrently
  const getExecutionLayers = useCallback((nodes: Node[], edges: Edge[]): string[][] => {
    console.log('[getExecutionLayers] Finding execution order for nodes:', nodes.map(n => n.id));
    console.log('[getExecutionLayers] Edges:', edges.map(e => `${e.source} -> ${e.target}`));
    
    // Find the start node
    const startNode = nodes.find(n => n.id === '__start__');
    if (!startNode) {
      addLog({ level: 'error', message: 'No start node found in graph', source: 'system' });
      return [];
    }

    // Check if this is a supervisor pattern (has 'supervisor' node with conditional edges)
    const supervisorNode = nodes.find(n => n.id === 'supervisor');
    const hasConditionalEdges = edges.some(e => e.conditional || e.data?.conditional);
    
    if (supervisorNode && hasConditionalEdges) {
      console.log('[getExecutionLayers] Detected supervisor pattern');
      return getSupervisorExecutionLayers(nodes, edges, startNode, supervisorNode, addLog);
    }
    
    // Otherwise, use topological sort for sequential/DAG execution
    console.log('[getExecutionLayers] Using topological sort for sequential execution');
    return getTopologicalExecutionLayers(nodes, edges, startNode, addLog);
  }, [addLog, getSupervisorExecutionLayers, getTopologicalExecutionLayers]);

  // Handler for run button - Mock execution
  const handleRun = useCallback(async (
    selectedNode: Node | null,
    allNodes: Node[],
    allEdges: Edge[]
  ) => {
    console.log('[useGraphEditor] handleRun called');
    console.log('[useGraphEditor] isExecuting:', isExecuting);
    console.log('[useGraphEditor] allNodes:', allNodes);
    console.log('[useGraphEditor] allEdges:', allEdges);
    
    // Prevent concurrent executions
    if (isExecuting) {
      console.warn('[useGraphEditor] Execution already in progress - blocking concurrent run');
      addLog({ level: 'warning', message: 'Execution already in progress. Please wait for current execution to complete.', source: 'system' });
      return;
    }
    
    console.log('[useGraphEditor] Starting new execution...');

    // Simulate node execution
    const executeNode = async (node: Node): Promise<boolean> => {
      const nodeName = node.data.label?.props?.children?.[1]?.props?.children || node.data.title || node.id;
      
      console.log(`[useGraphEditor] Executing node: ${nodeName} (${node.id})`);
      
      // Add to executing nodes
      setExecutingNodeIds(prev => [...prev, node.id]);
      
      // Log start of execution
      addLog({
        level: 'info',
        message: `Starting execution of node: ${nodeName}`,
        source: nodeName,
      });

      // Simulate processing time (1-3 seconds)
      const processingTime = Math.random() * 2000 + 1000;
      await new Promise(resolve => setTimeout(resolve, processingTime));

      // Random outcome (mostly success, occasional warnings)
      const rand = Math.random();
      
      if (node.id === '__start__') {
        addLog({
          level: 'success',
          message: `Graph execution started`,
          source: nodeName,
        });
      } else if (node.id === '__end__') {
        addLog({
          level: 'success',
          message: `Graph execution completed successfully`,
          source: nodeName,
        });
      } else if (rand < 0.7) {
        // Success case
        const successMessages = [
          `Processed data successfully`,
          `Task completed without errors`,
          `Output generated and validated`,
          `All checks passed`,
          `Execution successful`,
        ];
        addLog({
          level: 'success',
          message: successMessages[Math.floor(Math.random() * successMessages.length)],
          source: nodeName,
        });
      } else if (rand < 0.9) {
        // Warning case
        const warningMessages = [
          `Execution completed with minor warnings`,
          `Performance threshold exceeded`,
          `Memory usage higher than expected`,
          `Non-critical validation failed`,
        ];
        addLog({
          level: 'warning',
          message: warningMessages[Math.floor(Math.random() * warningMessages.length)],
          source: nodeName,
        });
      } else {
        // Error case (rare, and we'll continue anyway for demo)
        addLog({
          level: 'error',
          message: `Recoverable error occurred, continuing execution`,
          source: nodeName,
        });
      }

      // Remove from executing nodes
      setExecutingNodeIds(prev => prev.filter(id => id !== node.id));
      console.log(`[useGraphEditor] Completed execution of node: ${nodeName}`);
      return true;
    };

    console.log('[useGraphEditor] Setting isExecuting to true');
    setIsExecuting(true);
    clearLogs();
    
    addLog({
      level: 'info',
      message: '========================================',
      source: 'system',
    });
    addLog({
      level: 'info',
      message: 'Starting graph execution...',
      source: 'system',
    });
    addLog({
      level: 'info',
      message: '========================================',
      source: 'system',
    });

    console.log('[useGraphEditor] Getting execution layers...');
    // Get execution layers
    const executionLayers = getExecutionLayers(allNodes, allEdges);
    
    if (executionLayers.length === 0) {
      console.error('[useGraphEditor] Failed to determine execution order');
      addLog({ level: 'error', message: 'Failed to determine execution order', source: 'system' });
      setIsExecuting(false);
      return;
    }
    
    console.log('[useGraphEditor] Execution layers:', executionLayers);

    const totalNodes = executionLayers.reduce((sum, layer) => sum + layer.length, 0);
    addLog({
      level: 'info',
      message: `Execution plan: ${totalNodes} nodes in ${executionLayers.length} layers`,
      source: 'system',
    });

    // Track supervisor execution count for better logging
    let supervisorExecutionCount = 0;
    
    // Execute nodes layer by layer
    for (let layerIndex = 0; layerIndex < executionLayers.length; layerIndex++) {
      const layer = executionLayers[layerIndex];
      console.log(`[useGraphEditor] Executing layer ${layerIndex + 1}/${executionLayers.length}:`, layer);
      
      if (layer.length === 1) {
        // Single node in layer - execute sequentially
        const nodeId = layer[0];
        const node = allNodes.find(n => n.id === nodeId);
        if (node) {
          let nodeName = node.data.label?.props?.children?.[1]?.props?.children || node.data.title || node.id;
          
          // Add context for supervisor re-execution
          if (nodeId === 'supervisor') {
            supervisorExecutionCount++;
            if (supervisorExecutionCount === 1) {
              nodeName += ' (routing tasks)';
            } else if (supervisorExecutionCount === 2) {
              nodeName += ' (collecting results)';
            }
          }
          
          addLog({
            level: 'info',
            message: `→ Layer ${layerIndex + 1}/${executionLayers.length}: Executing ${nodeName}`,
            source: 'system',
          });
          await executeNode(node);
        }
      } else {
        // Multiple nodes in layer - execute concurrently
        const nodeNames = layer
          .map(id => {
            const node = allNodes.find(n => n.id === id);
            return node?.data.label?.props?.children?.[1]?.props?.children || node?.data.title || id;
          })
          .join(', ');
        
        addLog({
          level: 'info',
          message: `→ Layer ${layerIndex + 1}/${executionLayers.length}: Executing ${layer.length} nodes concurrently [${nodeNames}]`,
          source: 'system',
        });

        // Execute all nodes in this layer concurrently
        const layerPromises = layer.map(nodeId => {
          const node = allNodes.find(n => n.id === nodeId);
          return node ? executeNode(node) : Promise.resolve(false);
        });

        await Promise.all(layerPromises);
        
        addLog({
          level: 'success',
          message: `✓ Layer ${layerIndex + 1} completed (${layer.length} nodes)`,
          source: 'system',
        });
      }
      
      // Small delay between layers
      if (layerIndex < executionLayers.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }

    addLog({
      level: 'info',
      message: '========================================',
      source: 'system',
    });
    addLog({
      level: 'success',
      message: '✓ Graph execution completed!',
      source: 'system',
    });
    addLog({
      level: 'info',
      message: '========================================',
      source: 'system',
    });

    console.log('[useGraphEditor] Execution completed, setting isExecuting to false');
    setIsExecuting(false);
  }, [isExecuting, addLog, clearLogs, getExecutionLayers, getSupervisorExecutionLayers, getTopologicalExecutionLayers]);

  // Handler for adding nodes
  const handleNodeAdd = useCallback((
    nodeData: { id: string; title: string; icon: string; type: string; description?: string; nodeType?: string },
    setNodes: (callback: (nodes: Node[]) => Node[]) => void
  ) => {
    const currentCount = nodeCounter[nodeData.id] || 1;
    const nodeId = `${nodeData.id}-${currentCount}`;

    setNodeCounter(prev => ({
      ...prev,
      [nodeData.id]: currentCount + 1
    }));

    // Check if it's a testing node (prompt injection or other testing types)
    if (nodeData.type === 'testing' || nodeData.id === 'prompt-inject' || nodeData.nodeType === 'prompt_injection') {
      const newNode: Node = {
        id: nodeId,
        type: 'promptInject',
        position: {
          x: Math.random() * 400 + 100,
          y: Math.random() * 400 + 100,
        },
        data: {
          icon: nodeData.icon,
          title: nodeData.title,
          nodeType: nodeData.nodeType || nodeData.id, // Store the node type for API calls
        },
        draggable: true,
      };
      setNodes((nds) => [...nds, newNode]);
    } else {
      const newNode: Node = {
        id: nodeId,
        type: 'default',
        position: {
          x: Math.random() * 400 + 100,
          y: Math.random() * 400 + 100,
        },
        data: {
          label: (
            <div className="flex items-center gap-2">
              <span>{nodeData.icon}</span>
              <span>{nodeData.title}</span>
            </div>
          ),
        },
      };
      setNodes((nds) => [...nds, newNode]);
    }
  }, [nodeCounter, setNodeCounter]);

  return {
    isDirectoryOpen,
    setIsDirectoryOpen,
    isLogPanelOpen,
    setIsLogPanelOpen,
    handleRun,
    handleNodeAdd,
    executionLogs,
    isExecuting,
    executingNodeIds,
    clearLogs,
    addLog,
  };
}

