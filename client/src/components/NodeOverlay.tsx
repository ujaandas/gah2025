"use client";

import Node from './Node';

interface NodeData {
  id: string;
  title: string;
  description?: string;
  position: { x: number; y: number };
}

export default function NodeOverlay() {
  const nodes: NodeData[] = [
    {
      id: "node-1",
      title: "Start Node",
      description: "This is the starting point",
      position: { x: 100, y: 100 }
    },
    {
      id: "node-2",
      title: "Process Node",
      description: "Processing data here",
      position: { x: 400, y: 150 }
    },
    {
      id: "node-3",
      title: "Decision Node",
      description: "Make a decision",
      position: { x: 250, y: 300 }
    },
    {
      id: "node-4",
      title: "End Node",
      description: "Final destination",
      position: { x: 500, y: 350 }
    }
  ];

  return (
    <div className="relative w-full h-full">
      {nodes.map((node) => (
        <Node
          key={node.id}
          id={node.id}
          title={node.title}
          description={node.description}
          position={node.position}
        />
      ))}
    </div>
  );
}
