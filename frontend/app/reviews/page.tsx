import React from 'react';

export default function ReviewsPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Pull Request Reviews</h1>
      <p className="text-gray-400 mb-8">History of AI-powered code reviews across all repositories.</p>
      
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <h2 className="text-lg font-medium text-white mb-4">Recent Reviews</h2>
        
        <div className="space-y-4">
          <div className="border border-gray-700 rounded-md p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="text-md font-medium text-white">PR #1025: Update auth flow</h3>
                <p className="text-sm text-gray-400">acme-corp/backend-api • Reviewed 2 hours ago</p>
              </div>
              <div className="flex space-x-2">
                <span className="px-3 py-1 bg-red-500/10 text-red-400 text-xs rounded border border-red-500/20">2 Critical</span>
                <span className="px-3 py-1 bg-yellow-500/10 text-yellow-400 text-xs rounded border border-yellow-500/20">4 Warnings</span>
              </div>
            </div>
            <p className="text-sm text-gray-300 mt-3 border-t border-gray-700 pt-3">
              Detected hardcoded API secrets in authentication middleware and an unescaped SQL query payload.
            </p>
          </div>

          <div className="border border-gray-700 rounded-md p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="text-md font-medium text-white">PR #1024: Fix dashboard layout</h3>
                <p className="text-sm text-gray-400">acme-corp/frontend-app • Reviewed 5 hours ago</p>
              </div>
              <div className="flex space-x-2">
                <span className="px-3 py-1 bg-green-500/10 text-green-400 text-xs rounded border border-green-500/20">Passed</span>
              </div>
            </div>
            <p className="text-sm text-gray-300 mt-3 border-t border-gray-700 pt-3">
              No security or performance issues detected. Code is clean and meets style guidelines.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
