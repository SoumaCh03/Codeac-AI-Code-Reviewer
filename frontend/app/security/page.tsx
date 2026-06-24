import React from 'react';

export default function SecurityPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Security Posture</h1>
      <p className="text-gray-400 mb-8">Overview of security vulnerabilities detected across all repositories.</p>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h2 className="text-lg font-medium text-white mb-4">Vulnerability Breakdown</h2>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b border-gray-700 pb-3">
              <span className="text-gray-300">Hardcoded Secrets</span>
              <span className="font-bold text-red-400">2</span>
            </div>
            <div className="flex justify-between items-center border-b border-gray-700 pb-3">
              <span className="text-gray-300">Cross-Site Scripting (XSS)</span>
              <span className="font-bold text-yellow-400">1</span>
            </div>
            <div className="flex justify-between items-center border-b border-gray-700 pb-3">
              <span className="text-gray-300">SQL Injection</span>
              <span className="font-bold text-gray-500">0</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Insecure Direct Object Reference</span>
              <span className="font-bold text-gray-500">0</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h2 className="text-lg font-medium text-white mb-4">Active Incidents</h2>
          <div className="flex flex-col items-center justify-center h-40 text-center">
            <div className="text-green-500 mb-2">
              <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-white font-medium">All clear</p>
            <p className="text-sm text-gray-400 mt-1">No critical incidents require immediate attention.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
