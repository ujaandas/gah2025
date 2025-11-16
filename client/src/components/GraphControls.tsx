import type { Node, Edge } from 'reactflow';

interface GraphControlsProps {
  selectedNode: Node | null;
  draggedNode: Node | null;
  hoveredEdge: string | null;
  edges: Edge[];
  onAddNodeClick: () => void;
  onDeleteNode: () => void;
}

/**
 * Floating controls for the graph editor (add button, delete button, hints)
 */
export default function GraphControls({
  selectedNode,
  draggedNode,
  hoveredEdge,
  edges,
  onAddNodeClick,
  onDeleteNode,
}: GraphControlsProps) {
  // Check if draggedNode is already part of the graph
  const isNodeConnected = draggedNode 
    ? edges.some(e => e.target === draggedNode.id) && edges.some(e => e.source === draggedNode.id)
    : false;

  return (
    <>
      {/* Floating Add Node Button */}
      <button
        onClick={onAddNodeClick}
        className="fixed top-24 left-8 text-white w-12 h-12 rounded-full shadow-lg hover:shadow-xl transition-all font-medium flex items-center justify-center z-[1000]"
        style={{ background: '#1f2937' }}
        onMouseEnter={(e) => e.currentTarget.style.background = '#111827'}
        onMouseLeave={(e) => e.currentTarget.style.background = '#1f2937'}
      >
        <span className="text-2xl">+</span>
      </button>

      {/* Delete Node Button (shown when prompt inject node is selected) */}
      {selectedNode && selectedNode.type === 'promptInject' && (
        <div className="fixed top-24 right-8 bg-white border-2 border-gray-300 rounded-lg shadow-lg p-4 z-[1000]">
          <p className="text-sm font-semibold mb-2 text-gray-700">Prompt Inject Node Selected</p>
          <button
            onClick={onDeleteNode}
            className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-all flex items-center justify-center gap-2"
          >
            <span>🗑️</span>
            <span>Delete Node</span>
          </button>
          <p className="text-xs text-gray-500 mt-2 text-center">Or press Delete/Backspace</p>
        </div>
      )}

      {/* Drag and Drop Hint - only show if node is not yet connected */}
      {draggedNode && !isNodeConnected && (
        <div className="fixed top-44 right-8 bg-blue-50 border-2 border-blue-300 rounded-lg shadow-lg p-4 z-[1000]">
          <p className="text-sm font-semibold text-blue-700 flex items-center gap-2">
            <span>💡</span>
            <span>Drop on any edge to inject</span>
          </p>
          {hoveredEdge && (
            <p className="text-xs text-green-600 mt-2 flex items-center gap-1">
              <span>✓</span>
              <span>Valid drop location!</span>
            </p>
          )}
        </div>
      )}
    </>
  );
}

