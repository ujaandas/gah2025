import { useEffect, useCallback } from 'react';
import type { Node } from 'reactflow';

/**
 * Hook to handle keyboard shortcuts (e.g., delete/backspace for node deletion)
 */
export function useKeyboardShortcuts(
  selectedNode: Node | null,
  handleDeleteNode: () => void
) {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    if ((event.key === 'Delete' || event.key === 'Backspace') && 
        selectedNode?.type === 'promptInject') {
      event.preventDefault();
      handleDeleteNode();
    }
  }, [selectedNode, handleDeleteNode]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);
}

