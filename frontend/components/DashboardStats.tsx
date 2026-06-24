export function DashboardStats() {
  const stats = [
    { name: "Total Repositories", value: "24", change: "+2", changeType: "positive" },
    { name: "PRs Reviewed", value: "1,204", change: "+12.5%", changeType: "positive" },
    { name: "Critical Findings", value: "3", change: "-2", changeType: "positive" },
    { name: "Avg Review Time", value: "1.2m", change: "-0.4m", changeType: "positive" },
  ];

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((item) => (
        <div
          key={item.name}
          className="relative overflow-hidden rounded-lg bg-white px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6 border border-gray-100"
        >
          <dt>
            <p className="truncate text-sm font-medium text-gray-500">{item.name}</p>
          </dt>
          <dd className="flex items-baseline pb-6 sm:pb-7">
            <p className="text-2xl font-semibold text-gray-900">{item.value}</p>
            <p
              className={`ml-2 flex items-baseline text-sm font-semibold ${
                item.changeType === "positive" ? "text-green-600" : "text-red-600"
              }`}
            >
              {item.change}
            </p>
          </dd>
        </div>
      ))}
    </div>
  );
}
