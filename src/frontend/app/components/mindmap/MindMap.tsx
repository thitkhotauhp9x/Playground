import { useState, useCallback } from 'react';
import {
  ReactFlow,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  NodeToolbar,
  Background,
  ReactFlowProvider
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  { id: 'n1', position: { x: 0, y: 0 }, data: { label: 'Node 1' }, type: 'node-with-toolbar'},
  { id: 'n2', position: { x: 0, y: 100 }, data: { label: 'Node 2' }, type: 'node-with-toolbar'},
];

const initialEdges = [
  { id: 'n1-n2', source: 'n1', target: 'n2',     type: 'default',
    style: {
      stroke: '#555',
      strokeWidth: 2,
    },}];

const nodeTypes = {
  'node-with-toolbar': NodeWithToolbar,
};

function NodeWithToolbar({ data }) {
  return (
    <>
      <NodeToolbar
        isVisible={data.forceToolbarVisible || undefined}
        position={data.toolbarPosition}
        align={data.align}
      >
        <button>add</button>
        <button>delete</button>
      </NodeToolbar>
      <div>{data?.label}</div>
    </>
  );
}

export default function MindMap() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);

  const onNodesChange = useCallback((changes) => setNodes((nodesSnapshot) => applyNodeChanges(changes, nodesSnapshot)), []);
  const onEdgesChange = useCallback((changes) => setEdges((edgesSnapshot) => applyEdgeChanges(changes, edgesSnapshot)), []);
  const onConnect = useCallback((params) => setEdges((edgesSnapshot) => addEdge(params, edgesSnapshot)), []);

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlowProvider>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          colorMode="system"
          fitView
        >
          <Background />
        </ReactFlow>
      </ReactFlowProvider>
    </div>
  );
}
