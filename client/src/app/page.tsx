"use client";

import { useState } from 'react';
import NodeDirectory from '@/components/NodeDirectory';
import TopBar from '@/components/TopBar';

export default function Home() {
  const [isDirectoryOpen, setIsDirectoryOpen] = useState(false);

  return (
    <div
      className="min-h-screen w-full"
      style={{
        backgroundImage: 'radial-gradient(circle, #d1d5db 1px, transparent 1px)',
        backgroundSize: '20px 20px'
      }}
    >
      {/* Floating Add Node Button */}
      <button
        onClick={() => setIsDirectoryOpen(true)}
        className="fixed top-8 left-8 bg-blue-600 hover:bg-blue-700 text-white w-12 h-12 rounded-full shadow-lg hover:shadow-xl transition-all font-medium flex items-center justify-center"
      >
        <span className="text-2xl">+</span>
      </button>

      {/* Top Bar */}
      <TopBar />

      {/* Node Directory Modal */}
      <NodeDirectory
        isOpen={isDirectoryOpen}
        onClose={() => setIsDirectoryOpen(false)}
      />
    </div>
  );
}
