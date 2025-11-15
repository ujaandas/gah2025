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
      title: "Prompt Inject Node",
      description: "Inject prompts into the workflow",
      position: { x: 100, y: 100 }
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
