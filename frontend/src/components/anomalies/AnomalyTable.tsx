import { useState, useMemo } from 'react';
import { Search, Filter } from 'lucide-react';
import { AnomalyResult } from '../../types/api';
import { Badge } from '../ui/Badge';
import { formatDate, formatCurrency, formatNumber } from '../../lib/utils';

interface AnomalyTableProps {
  anomalies: AnomalyResult[];
  isLoading?: boolean;
}

export function AnomalyTable({ anomalies, isLoading }: AnomalyTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [methodFilter, setMethodFilter] = useState('ALL');

  const uniqueMethods = useMemo(() => {
    const set = new Set<string>();
    anomalies.forEach((a) => {
      if (a.detection_method) set.add(a.detection_method);
    });
    return Array.from(set);
  }, [anomalies]);

  const filtered = useMemo(() => {
    return anomalies.filter((item) => {
      const matchesSearch =
        item.anomaly_id.toString().includes(searchTerm.trim()) ||
        item.store_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.detection_method.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesMethod =
        methodFilter === 'ALL' || item.detection_method === methodFilter;

      return matchesSearch && matchesMethod;
    });
  }, [anomalies, searchTerm, methodFilter]);

  return (
    <div className="space-y-4">
      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search by anomaly ID or store ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3.5 py-2 bg-slate-900 border border-slate-700/80 rounded-lg text-xs md:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-300">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-400 font-mono uppercase text-[10px]">Method:</span>
            <select
              value={methodFilter}
              onChange={(e) => setMethodFilter(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="ALL" className="bg-slate-900">All Methods</option>
              {uniqueMethods.map((m) => (
                <option key={m} value={m} className="bg-slate-900">
                  {m}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-950/40 text-[11px] font-mono uppercase tracking-wider text-slate-400">
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Tx Date</th>
                <th className="py-3 px-4">Store</th>
                <th className="py-3 px-4">Detection Method</th>
                <th className="py-3 px-4 text-right">Revenue</th>
                <th className="py-3 px-4 text-right">Transactions</th>
                <th className="py-3 px-4 text-right">Anomaly Score</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Detected At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {isLoading ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-400 font-mono">
                    Loading retail anomaly observations from PostgreSQL...
                  </td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-500">
                    No anomalies match current filter criteria
                  </td>
                </tr>
              ) : (
                filtered.map((item) => (
                  <tr
                    key={item.anomaly_id}
                    className="hover:bg-slate-800/40 transition-colors group font-mono text-[11px]"
                  >
                    <td className="py-3 px-4 font-bold text-amber-400">
                      #{item.anomaly_id}
                    </td>
                    <td className="py-3 px-4 text-slate-300">
                      {item.transaction_date}
                    </td>
                    <td className="py-3 px-4 font-sans font-medium text-slate-200">
                      {item.store_id}
                    </td>
                    <td className="py-3 px-4">
                      <span className="bg-slate-800 px-2 py-0.5 rounded border border-slate-700/60 text-slate-300 text-[10px]">
                        {item.detection_method}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-medium text-slate-200">
                      {formatCurrency(item.total_revenue)}
                    </td>
                    <td className="py-3 px-4 text-right text-slate-400">
                      {formatNumber(item.total_transactions)}
                    </td>
                    <td className="py-3 px-4 text-right">
                      {item.anomaly_score !== null ? (
                        <span className="text-rose-400 font-bold">
                          {item.anomaly_score.toFixed(4)}
                        </span>
                      ) : (
                        '—'
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant="status" value={item.anomaly_status}>
                        {item.anomaly_status}
                      </Badge>
                    </td>
                    <td className="py-3 px-4 text-slate-400 text-[10px] whitespace-nowrap">
                      {formatDate(item.detected_at)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
