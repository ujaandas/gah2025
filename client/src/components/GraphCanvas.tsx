"use client";

import { useState, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  BackgroundVariant,
  type Node,
  type Edge,
  type Connection,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useTheme } from 'next-themes';

interface GraphCanvasProps {
  nodes: Node[];
  edges: Edge[];
  nodeTypes: any;
  onNodesChange: any;
  onEdgesChange: any;
  onConnect: (connection: Connection) => void;
  onNodeClick: (event: React.MouseEvent, node: Node) => void;
  onNodeDragStart: (event: React.MouseEvent, node: Node) => void;
  onNodeDrag: (event: React.MouseEvent, node: Node) => void;
  onNodeDragStop: (event: React.MouseEvent, node: Node) => void;
}

/**
 * The main React Flow canvas component with n8n-inspired styling
 */
export default function GraphCanvas({
  nodes,
  edges,
  nodeTypes,
  onNodesChange,
  onEdgesChange,
  onConnect,
  onNodeClick,
  onNodeDragStart,
  onNodeDrag,
  onNodeDragStop,
}: GraphCanvasProps) {
  const { theme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  useEffect(() => {
    console.log('[GraphCanvas] Nodes:', nodes);
    console.log('[GraphCanvas] Edges:', edges);
  }, [nodes, edges]);
  
  // Use resolvedTheme to get the actual theme (considering system preference)
  // Default to light theme during SSR to prevent hydration mismatch
  const isDark = mounted && (resolvedTheme === 'dark' || theme === 'dark');

  return (
    <div className="w-full h-full absolute top-0 left-0" style={{ minHeight: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onNodeDragStart={onNodeDragStart}
        onNodeDrag={onNodeDrag}
        onNodeDragStop={onNodeDragStop}
        nodeTypes={nodeTypes}
        className={isDark ? "bg-zinc-950" : "bg-zinc-50"}
        minZoom={0.1}
        maxZoom={4}
        attributionPosition="bottom-right"
        proOptions={{ hideAttribution: true }}
        defaultEdgeOptions={{
          type: 'smoothstep',
          animated: false,
          style: {
            strokeWidth: 2,
            stroke: isDark ? '#52525b' : '#d4d4d8',
          },
        }}
        connectionLineStyle={{
          strokeWidth: 2,
          stroke: isDark ? '#8b5cf6' : '#7c3aed',
        }}
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={20}
          size={1}
          color={isDark ? '#27272a' : '#e4e4e7'}
          className="transition-colors"
        />
        <Controls
          className={`
            ${isDark 
              ? '!bg-zinc-900 !border-zinc-800 [&>button]:!bg-zinc-900 [&>button]:!border-zinc-800 [&>button:hover]:!bg-zinc-800 [&>button]:!text-zinc-300' 
              : '!bg-white !border-zinc-200 [&>button]:!bg-white [&>button]:!border-zinc-200 [&>button:hover]:!bg-zinc-50'
            }
            !shadow-lg !rounded-xl [&>button]:!rounded-lg [&>button]:!transition-all
          `}
          showInteractive={false}
        />
      </ReactFlow>
    </div>
  );
}
