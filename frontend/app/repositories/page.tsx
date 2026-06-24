import React from 'react';

export default function RepositoriesPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Repositories</h1>
      <p className="text-gray-400 mb-8">Manage and view connected GitHub repositories.</p>
      
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium text-white">Connected Repositories</h2>
          <a 
            href={process.env.NEXT_PUBLIC_GITHUB_APP_URL || "https://github.com/apps/codeac-ai-reviewer/installations/new"}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm transition-colors inline-block"
          >
            Connect New Repository
          </a>
        </div>
        
        <div className="space-y-4">
          {/* Placeholder for repos list */}
          <div className="border border-gray-700 rounded-md p-4 flex justify-between items-center">
            <div>
              <h3 className="text-md font-medium text-white">acme-corp/backend-api</h3>
              <p className="text-sm text-gray-400">Node.js API • Last review 2 hours ago</p>
            </div>
            <span className="px-3 py-1 bg-green-500/10 text-green-400 text-xs rounded-full border border-green-500/20">Active</span>
          </div>
          
          <div className="border border-gray-700 rounded-md p-4 flex justify-between items-center">
            <div>
              <h3 className="text-md font-medium text-white">acme-corp/frontend-app</h3>
              <p className="text-sm text-gray-400">React Frontend • Last review 5 hours ago</p>
            </div>
            <span className="px-3 py-1 bg-green-500/10 text-green-400 text-xs rounded-full border border-green-500/20">Active</span>
          </div>
        </div>
      </div>
    </div>
  );
}
