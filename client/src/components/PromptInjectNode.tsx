"use client";

import { Handle, Position, type NodeProps } from 'reactflow';

interface PromptInjectNodeData {
  icon: string;
  title: string;
  nodeType?: string;
  config?: Record<string, any>;
}

export default function PromptInjectNode({ id, data }: NodeProps<PromptInjectNodeData>) {
  return (
    <div className="bg-white border-2 border-orange-500 rounded-lg shadow-lg p-3 min-w-[200px]">
      {/* Input handle at top */}
      <Handle type="target" position={Position.Top} className="!bg-orange-500" />

      {/* Node Content */}
      <div className="flex items-center gap-2">
        <span className="text-2xl">{data.icon}</span>
        <span className="font-semibold text-gray-800 text-sm">{data.title}</span>
      </div>

      {/* Output handle at bottom */}
      <Handle type="source" position={Position.Bottom} className="!bg-orange-500" />
    </div>
  );
}
