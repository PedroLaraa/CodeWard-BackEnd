import type { FC } from "react";
import { PieChart, Pie, Cell, Tooltip } from "recharts";

type Vulnerability = {
  level?: string;
};

type ScanResult = {
  vulnerabilities: Vulnerability[];
};

type Props = {
  results: ScanResult[];
};

type LevelCount = {
  [key: string]: number;
};

const COLORS: { [key: string]: string } = {
  Critical: "#dc2626",
  High: "#f97316",
  Medium: "#facc15",
  Low: "#22c55e",
  None: "#3b82f6",
  Unknown: "#6b7280",
};

const calculateSeverityDistribution = (results: ScanResult[]): LevelCount => {
  const counts: LevelCount = {
    None: 0,
    Low: 0,
    Medium: 0,
    High: 0,
    Critical: 0,
    Unknown: 0,
  };

  results.forEach((res) => {
    res.vulnerabilities.forEach((vuln) => {
      const level = vuln.level ?? "Unknown";
      counts[level] = (counts[level] || 0) + 1;
    });
  });

  return counts;
};

export const DashboardSummary: FC<Props> = ({ results }) => {
  const severityStats = calculateSeverityDistribution(results);
  const total = Object.values(severityStats).reduce((a, b) => a + b, 0);
  const chartData = Object.entries(severityStats)
    .filter(([, count]) => count > 0)
    .map(([level, count]) => ({
      name: level,
      value: count,
    }));

  if (total === 0) return null;

  return (
    <div className="bg-gray-800 rounded-xl shadow-md p-6 mb-6">
      <h2 className="text-2xl font-semibold mb-4">📊 Resumo de Severidade</h2>
      <div className="flex flex-col md:flex-row gap-6 items-center">
        <div>
          <PieChart width={250} height={250}>
            <Pie
              data={chartData}
              dataKey="value"
              cx="50%"
              cy="50%"
              outerRadius={80}
              label
            >
              {chartData.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={COLORS[entry.name] || "#ccc"}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-2 gap-4 text-sm w-full">
          {Object.entries(severityStats).map(([level, count]) => (
            <div key={level}>
              <div className="font-bold text-white">{level}</div>
              <div className="text-gray-300">
                {count} ({((count / total) * 100).toFixed(1)}%)
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
