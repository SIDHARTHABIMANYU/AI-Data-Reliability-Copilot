import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { Card, CardHeader, CardTitle } from '../ui/Card';
import { PieChart as PieChartIcon } from 'lucide-react';

interface SeverityChartProps {
  highCount: number;
  openCount: number;
  resolvedCount: number;
  totalCount: number;
}

export function SeverityChart({
  highCount,
  openCount,
  resolvedCount,
  totalCount,
}: SeverityChartProps) {
  if (totalCount === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>
            <PieChartIcon className="w-4 h-4 text-sky-400" />
            Incident Distribution
          </CardTitle>
        </CardHeader>
        <div className="h-56 flex items-center justify-center text-xs text-slate-500 font-mono">
          No incident data recorded yet
        </div>
      </Card>
    );
  }

  const data = [
    { name: 'High Severity', value: highCount, color: '#f43f5e' },
    { name: 'Open (Med/Low)', value: Math.max(0, openCount - highCount), color: '#fbbf24' },
    { name: 'Resolved', value: resolvedCount, color: '#10b981' },
  ].filter((item) => item.value > 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <PieChartIcon className="w-4 h-4 text-sky-400" />
          Incident Breakdown
        </CardTitle>
        <span className="text-xs font-mono text-slate-400">{totalCount} Total</span>
      </CardHeader>

      <div className="h-56 w-full flex items-center">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={80}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} stroke="#0b111c" strokeWidth={2} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                borderColor: '#334155',
                borderRadius: '8px',
                fontSize: '12px',
                color: '#f8fafc',
              }}
              formatter={(value: number) => [`${value} incidents`, 'Count']}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center">
        <div>
          <div className="text-[11px] text-rose-400 font-medium">Critical / High</div>
          <div className="text-sm font-mono font-bold text-slate-200">{highCount}</div>
        </div>
        <div>
          <div className="text-[11px] text-amber-400 font-medium">Active Open</div>
          <div className="text-sm font-mono font-bold text-slate-200">{openCount}</div>
        </div>
        <div>
          <div className="text-[11px] text-emerald-400 font-medium">Resolved</div>
          <div className="text-sm font-mono font-bold text-slate-200">{resolvedCount}</div>
        </div>
      </div>
    </Card>
  );
}
