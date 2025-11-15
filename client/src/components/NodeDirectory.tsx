"use client";

import { useState } from 'react';

interface NodeDirectoryProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function NodeDirectory({ isOpen, onClose }: NodeDirectoryProps) {
  const [searchQuery, setSearchQuery] = useState('');

  if (!isOpen) return null;

  const coreNodes = [
    {
      id: 'extract-data',
      title: 'Extract Data',
      description: 'Extract key piece...',
      icon: '📤',
      color: 'bg-pink-50'
    },
    {
      id: 'output',
      title: 'Output',
      description: 'Exit point for...',
      icon: '⬆️',
      color: 'bg-gray-50'
    },
    {
      id: 'categorizer',
      title: 'Categorizer',
      description: 'Categorize data...',
      icon: '🎯',
      color: 'bg-pink-50'
    },
    {
      id: 'router',
      title: 'Router',
      description: 'Control workflow...',
      icon: '🔀',
      color: 'bg-gray-50'
    }
  ];

  const integrations = [
    {
      id: 'airtable',
      title: 'Airtable',
      description: 'Manage data in Airtable bases',
      icon: '🔷',
      badge: 'MCP',
      badgeColor: 'bg-blue-200 text-blue-700'
    },
    {
      id: 'gmail',
      title: 'Gmail',
      description: 'Read and send Gmail messages',
      icon: '📧',
      badge: 'MCP',
      badgeColor: 'bg-red-200 text-red-700'
    },
    {
      id: 'google-sheets',
      title: 'Google Sheets',
      description: 'Read and write Google Sheets data',
      icon: '📊',
      badge: 'MCP',
      badgeColor: 'bg-green-200 text-green-700'
    },
    {
      id: 'google-drive',
      title: 'Google Drive',
      description: 'Manage files in Google Drive',
      icon: '📁',
      badge: 'MCP',
      badgeColor: 'bg-blue-200 text-blue-700'
    },
    {
      id: 'google-calendar',
      title: 'Google Calendar',
      description: 'Manage Google Calendar events',
      icon: '📅',
      badge: 'MCP',
      badgeColor: 'bg-blue-200 text-blue-700'
    },
    {
      id: 'google-docs',
      title: 'Google Docs',
      description: 'Create and edit Google Docs',
      icon: '📄',
      badge: 'MCP',
      badgeColor: 'bg-blue-200 text-blue-700'
    },
    {
      id: 'google-ads',
      title: 'Google Ads',
      description: 'Manage Google Ads',
      icon: '📣',
      badge: 'MCP',
      badgeColor: 'bg-yellow-200 text-yellow-700'
    }
  ];

  return (
    <div className="fixed top-24 left-8 z-50">
      <div className="bg-white rounded-2xl shadow-2xl w-[600px] max-h-[600px] overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-800">Add Node</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <span className="text-2xl text-gray-600">×</span>
            </button>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400">
              🔍
            </div>
            <input
              type="text"
              placeholder="Search all nodes"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700"
            />
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[450px] p-6">
          {/* Core Nodes */}
          <div className="grid grid-cols-2 gap-3 mb-6">
            {coreNodes.map((node) => (
              <button
                key={node.id}
                className="flex items-start gap-3 p-4 rounded-xl border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all text-left"
              >
                <div className={`${node.color} p-3 rounded-lg text-2xl`}>
                  {node.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 text-sm mb-1">
                    {node.title}
                  </h3>
                  <p className="text-xs text-gray-600 truncate">
                    {node.description}
                  </p>
                </div>
              </button>
            ))}
          </div>

          {/* Integrations Section */}
          <div>
            <h3 className="text-sm font-semibold text-gray-500 mb-3">
              Integrations
            </h3>
            <div className="space-y-2">
              {integrations.map((integration) => (
                <button
                  key={integration.id}
                  className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-colors text-left group"
                >
                  <div className="bg-white border border-gray-200 p-2 rounded-lg text-2xl">
                    {integration.icon}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 text-sm mb-1">
                      {integration.title}
                    </h3>
                    <p className="text-xs text-gray-600">
                      {integration.description}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`${integration.badgeColor} px-2 py-1 rounded-md text-xs font-medium`}>
                      {integration.badge}
                    </span>
                    <span className="text-gray-400 group-hover:text-gray-600">›</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
