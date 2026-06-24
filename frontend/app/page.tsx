import { DashboardStats } from "@/components/DashboardStats";

export default function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
          Dashboard Overview
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          A high-level view of your organization&apos;s code quality and security.
        </p>
      </div>

      <DashboardStats />

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="bg-white rounded-lg shadow border border-gray-100 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Reviews</h3>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-md">
                <div>
                  <p className="font-medium text-gray-900">PR #{1024 + i}: Update auth flow</p>
                  <p className="text-sm text-gray-500">acme-corp/backend-api</p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">
                    2 Critical
                  </span>
                  <span className="inline-flex items-center rounded-md bg-yellow-50 px-2 py-1 text-xs font-medium text-yellow-800 ring-1 ring-inset ring-yellow-600/20">
                    4 Warnings
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow border border-gray-100 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Security Posture</h3>
          <div className="space-y-4">
             <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">SQL Injection</span>
                <span className="font-medium text-gray-900">0</span>
             </div>
             <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Cross-Site Scripting (XSS)</span>
                <span className="font-medium text-gray-900">1</span>
             </div>
             <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Hardcoded Secrets</span>
                <span className="font-medium text-gray-900">2</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
