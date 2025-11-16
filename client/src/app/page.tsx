"use client";

import { useMemo, useCallback, useEffect } from 'react';
import {
  addEdge,
  useNodesState,
  useEdgesState,
  type Connection,
  useReactFlow,
  ReactFlowProvider,
} from 'reactflow';
import 'reactflow/dist/style.css';

import NodeDirectory from '@/components/NodeDirectory';
import TopBar from '@/components/TopBar';
import LogPanel from '@/components/LogPanel';
import PromptInjectNode from '@/components/PromptInjectNode';
import GraphCanvas from '@/components/GraphCanvas';
import GraphControls from '@/components/GraphControls';

import { mockGraphStructure } from '@/lib/data/mockGraphData';
import { convertGraphStructure } from '@/lib/utils/graphConverter';
import { useGraphEditor } from '@/hooks/useGraphEditor';
import { useNodeSelection } from '@/hooks/useNodeSelection';
import { useNodeDragAndDrop } from '@/hooks/useNodeDragAndDrop';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

// Convert the mock graph structure
const { nodes: initialNodes, edges: initialEdges } = convertGraphStructure(mockGraphStructure);



function GraphEditor() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const { fitView } = useReactFlow();

  // Custom hooks for managing state and behavior
  const {
    isDirectoryOpen,
    setIsDirectoryOpen,
    isLogPanelOpen,
    setIsLogPanelOpen,
    promptData,
    setPromptData,
    handleRun,
    handleNodeAdd: handleNodeAddBase,
    executionLogs,
    isExecuting,
    executingNodeIds,
    clearLogs,
  } = useGraphEditor();

  const {
    selectedNode,
    onNodeClick,
    handleDeleteNode,
  } = useNodeSelection(edges, setNodes, setEdges, promptData, setPromptData);

  const {
    draggedNode,
    hoveredEdge,
    onNodeDragStart,
    onNodeDrag,
    onNodeDragStop,
  } = useNodeDragAndDrop(nodes, edges, initialEdges, setNodes, setEdges, fitView);

  // Keyboard shortcuts
  useKeyboardShortcuts(selectedNode, handleDeleteNode);

  // Update node styles when executing
  useEffect(() => {
    if (executingNodeIds.length > 0) {
      setNodes((nds) =>
        nds.map((node) => {
          if (executingNodeIds.includes(node.id)) {
            return {
              ...node,
              style: {
                ...node.style,
                border: '3px solid #3b82f6',
                boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)',
                animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
              },
            };
          }
          return {
            ...node,
            style: {
              ...node.style,
              border: undefined,
              boxShadow: undefined,
              animation: undefined,
            },
          };
        })
      );
    } else {
      // Reset all node styles when not executing
      setNodes((nds) =>
        nds.map((node) => ({
          ...node,
          style: {
            ...node.style,
            border: undefined,
            boxShadow: undefined,
            animation: undefined,
          },
        }))
      );
    }
  }, [executingNodeIds, setNodes]);

  // Update edge styles when executing - animate edges connected to executing nodes
  useEffect(() => {
    if (executingNodeIds.length > 0) {
      setEdges((eds) =>
        eds.map((edge) => {
          // Store original style if not already stored
          const originalStyle = (edge as any).originalStyle || edge.style;
          
          // Animate edges that connect TO currently executing nodes
          if (executingNodeIds.includes(edge.target)) {
            return {
              ...edge,
              animated: true,
              style: {
                ...originalStyle,
                stroke: '#3b82f6',
                strokeWidth: 3,
              },
              originalStyle,
            } as any;
          }
          return {
            ...edge,
            animated: false,
            style: originalStyle,
            originalStyle,
          } as any;
        })
      );
    } else {
      // Reset all edge styles when not executing
      setEdges((eds) =>
        eds.map((edge) => {
          const originalStyle = (edge as any).originalStyle || edge.style;
          return {
            ...edge,
            animated: false,
            style: originalStyle,
            originalStyle,
          } as any;
        })
      );
    }
  }, [executingNodeIds, setEdges]);

  // Define custom node types
  const nodeTypes = useMemo(() => ({
    promptInject: PromptInjectNode,
  }), []);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Wrap handleNodeAdd to pass setNodes
  const handleNodeAdd = useCallback((nodeData: { id: string; title: string; icon: string; type: string }) => {
    handleNodeAddBase(nodeData, setNodes);
  }, [handleNodeAddBase, setNodes]);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      {/* React Flow Canvas */}
      <GraphCanvas
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onNodeDragStart={onNodeDragStart}
        onNodeDrag={onNodeDrag}
        onNodeDragStop={onNodeDragStop}
      />

      {/* Graph Controls (Add, Delete, Hints) */}
      <GraphControls
        selectedNode={selectedNode}
        draggedNode={draggedNode}
        hoveredEdge={hoveredEdge}
        onAddNodeClick={() => setIsDirectoryOpen(true)}
        onDeleteNode={handleDeleteNode}
      />

      {/* Top Bar */}
      <TopBar 
        onRun={() => handleRun(selectedNode, nodes, edges)} 
        isExecuting={isExecuting}
      />

      {/* Node Directory Modal */}
      <NodeDirectory
        isOpen={isDirectoryOpen}
        onClose={() => setIsDirectoryOpen(false)}
        onNodeAdd={handleNodeAdd}
      />

      {/* Log Panel */}
      <LogPanel
        isOpen={isLogPanelOpen}
        onToggle={() => setIsLogPanelOpen(!isLogPanelOpen)}
        logs={executionLogs}
        onClearLogs={clearLogs}
      />
    </div>
  );
}

export default function Home() {
  return (
    <ReactFlowProvider>
      <GraphEditor />
    </ReactFlowProvider>
  );
}
