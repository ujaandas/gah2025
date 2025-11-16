// Mock Graph Structure (matching API format)
export const mockGraphStructure = {
  nodes: {
    '__start__': {
      id: '__start__',
      name: 'Start',
      node_type: 'start',
      is_testing: false,
      metadata: { icon: '▶️' }
    },
    'supervisor': {
      id: 'supervisor',
      name: 'Supervisor',
      node_type: 'agent',
      is_testing: false,
      metadata: { icon: '👨‍💼', description: 'Routes tasks' }
    },
    'Excel': {
      id: 'Excel',
      name: 'Excel',
      node_type: 'agent',
      is_testing: false,
      metadata: { icon: '📊' }
    },
    'PowerPoint': {
      id: 'PowerPoint',
      name: 'PowerPoint',
      node_type: 'agent',
      is_testing: false,
      metadata: { icon: '📽️' }
    },
    'Browser': {
      id: 'Browser',
      name: 'Browser',
      node_type: 'agent',
      is_testing: false,
      metadata: { icon: '🌐' }
    },
    'Research': {
      id: 'Research',
      name: 'Research',
      node_type: 'agent',
      is_testing: false,
      metadata: { icon: '🔬' }
    },
    '__end__': {
      id: '__end__',
      name: 'End',
      node_type: 'end',
      is_testing: false,
      metadata: { icon: '⏹️' }
    }
  },
  edges: [
    { source: '__start__', target: 'supervisor', conditional: false, metadata: {} },
    { source: 'supervisor', target: 'Excel', conditional: true, metadata: { label: 'route' } },
    { source: 'supervisor', target: 'PowerPoint', conditional: true, metadata: { label: 'route' } },
    { source: 'supervisor', target: 'Browser', conditional: true, metadata: { label: 'route' } },
    { source: 'supervisor', target: 'Research', conditional: true, metadata: { label: 'route' } },
    { source: 'supervisor', target: '__end__', conditional: true, metadata: { label: 'finish' } },
    { source: 'Excel', target: 'supervisor', conditional: false, metadata: { label: 'return' } },
    { source: 'PowerPoint', target: 'supervisor', conditional: false, metadata: { label: 'return' } },
    { source: 'Browser', target: 'supervisor', conditional: false, metadata: { label: 'return' } },
    { source: 'Research', target: 'supervisor', conditional: false, metadata: { label: 'return' } }
  ],
  start_nodes: ['__start__'],
  end_nodes: ['__end__']
};

export type GraphStructure = typeof mockGraphStructure;

