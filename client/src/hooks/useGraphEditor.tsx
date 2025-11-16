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
  const [promptData, setPromptData] = useState<Record<string, string>>({});
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

  // Handler for updating prompt data
  const handlePromptChange = useCallback((nodeId: string, prompt: string) => {
    setPromptData((prev) => {
      const updated = { ...prev, [nodeId]: prompt };
      return updated;
    });
  }, []);

  // Find execution layers - groups of nodes that can run concurrently
  const getExecutionLayers = useCallback((nodes: Node[], edges: Edge[]): string[][] => {
    // Find the start node
    const startNode = nodes.find(n => n.id === '__start__');
    if (!startNode) {
      addLog({ level: 'error', message: 'No start node found in graph', source: 'system' });
      return [];
    }

    const layers: string[][] = [];
    
    // For supervisor pattern with cycles, we need a specific execution plan
    // Layer 1: Start node
    layers.push([startNode.id]);
    
    // Layer 2: Find nodes connected to start (typically supervisor)
    const fromStart = edges
      .filter(e => e.source === startNode.id)
      .map(e => e.target);
    if (fromStart.length > 0) {
      layers.push(fromStart);
    }
    
    // Layer 3: Find all agent nodes (nodes that are not start, end, or supervisor)
    const supervisorNode = nodes.find(n => n.id === 'supervisor');
    const endNode = nodes.find(n => n.id === '__end__');
    
    if (supervisorNode) {
      // Find all outgoing conditional edges from supervisor (these are the agents)
      const agentNodes = edges
        .filter(e => e.source === 'supervisor' && e.data?.conditional && e.target !== '__end__')
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
    }

    console.log('Execution layers:', layers);
    return layers;
  }, [addLog]);

  // Handler for run button - Mock execution
  const handleRun = useCallback(async (
    selectedNode: Node | null,
    allNodes: Node[],
    allEdges: Edge[]
  ) => {
    if (isExecuting) {
      addLog({ level: 'warning', message: 'Execution already in progress', source: 'system' });
      return;
    }

    // Simulate node execution
    const executeNode = async (node: Node): Promise<boolean> => {
      const nodeName = node.data.label?.props?.children?.[1]?.props?.children || node.data.title || node.id;
      
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
      return true;
    };

    setIsExecuting(true);
    clearLogs();
    
    // Open log panel to show execution progress
    setIsLogPanelOpen(true);
    
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

    // Get execution layers
    const executionLayers = getExecutionLayers(allNodes, allEdges);
    
    if (executionLayers.length === 0) {
      addLog({ level: 'error', message: 'Failed to determine execution order', source: 'system' });
      setIsExecuting(false);
      return;
    }

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

    setIsExecuting(false);
  }, [isExecuting, addLog, clearLogs, getExecutionLayers]);

  // Handler for adding nodes
  const handleNodeAdd = useCallback((
    nodeData: { id: string; title: string; icon: string; type: string },
    setNodes: (callback: (nodes: Node[]) => Node[]) => void
  ) => {
    const currentCount = nodeCounter[nodeData.id] || 1;
    const nodeId = `${nodeData.id}-${currentCount}`;

    setNodeCounter(prev => ({
      ...prev,
      [nodeData.id]: currentCount + 1
    }));

    if (nodeData.id === 'prompt-inject') {
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
          prompt: '',
          onPromptChange: handlePromptChange,
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
  }, [handlePromptChange, nodeCounter, setNodeCounter]);

  return {
    isDirectoryOpen,
    setIsDirectoryOpen,
    isLogPanelOpen,
    setIsLogPanelOpen,
    promptData,
    setPromptData,
    handlePromptChange,
    handleRun,
    handleNodeAdd,
    executionLogs,
    isExecuting,
    executingNodeIds,
    clearLogs,
  };
}

