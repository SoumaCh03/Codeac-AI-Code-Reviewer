import Link from "next/link";

export function Sidebar() {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
          Codeac
        </h1>
        <p className="text-sm text-gray-400 mt-1">Autonomous Review</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-2">
        <Link href="/" className="block px-4 py-2 rounded-md bg-gray-800 text-white">
          Overview
        </Link>
        <Link href="/repositories" className="block px-4 py-2 rounded-md hover:bg-gray-800 text-gray-300">
          Repositories
        </Link>
        <Link href="/reviews" className="block px-4 py-2 rounded-md hover:bg-gray-800 text-gray-300">
          PR Reviews
        </Link>
        <Link href="/security" className="block px-4 py-2 rounded-md hover:bg-gray-800 text-gray-300">
          Security
        </Link>
      </nav>
      
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500"></div>
          <div>
            <p className="text-sm font-medium">Codeac Admin</p>
            <p className="text-xs text-gray-400">Admin Dashboard</p>
          </div>
        </div>
      </div>
    </div>
  );
}
