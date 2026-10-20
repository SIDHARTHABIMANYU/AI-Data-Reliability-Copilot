import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Sparkles, Wrench, ArrowUpDown } from 'lucide-react';
import { Incident } from '../../types/api';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { formatDate } from '../../lib/utils';

interface IncidentTableProps {
  incidents: Incident[];
  isLoading?: boolean;
}

export function IncidentTable({ incidents, isLoading }: IncidentTableProps) {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [statusFilter, setStatusFilter] = useState<string>('ALL');

  const filteredIncidents = useMemo(() => {
    return incidents.filter((incident) => {
      const matchesSearch =
        incident.incident_id.toString().includes(searchTerm.trim()) ||
        incident.dataset.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.file_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.incident_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        incident.description.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesSeverity =
        severityFilter === 'ALL' || incident.severity.toUpperCase() === severityFilter;

      const matchesStatus =
        statusFilter === 'ALL' || incident.status.toUpperCase() === statusFilter;

      return matchesSearch && matchesSeverity && matchesStatus;
    });
  }, [incidents, searchTerm, severityFilter, statusFilter]);

  return (
    <div className="space-y-4">
      {/* Search and Filters toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search by ID, dataset, file, or type..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3.5 py-2 bg-slate-900 border border-slate-750 border-slate-700/80 rounded-lg text-xs md:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-300">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-400 font-mono uppercase text-[10px]">Severity:</span>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="ALL" className="bg-slate-900">All</option>
              <option value="HIGH" className="bg-slate-900">High</option>
              <option value="MEDIUM" className="bg-slate-900">Medium</option>
              <option value="LOW" className="bg-slate-900">Low</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-300">
            <span className="text-slate-400 font-mono uppercase text-[10px]">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="ALL" className="bg-slate-900">All</option>
              <option value="OPEN" className="bg-slate-900">Open</option>
              <option value="RESOLVED" className="bg-slate-900">Resolved</option>
            </select>
          </div>
        </div>
      </div>

      {/* Incident Table */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-950/40 text-[11px] font-mono uppercase tracking-wider text-slate-400">
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Dataset & File</th>
                <th className="py-3 px-4">Incident Type</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">
                  <span className="flex items-center gap-1">
                    Detected <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </span>
                </th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-400 font-mono">
                    Loading live incidents from PostgreSQL...
                  </td>
                </tr>
              ) : filteredIncidents.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">
                    No incidents match your filter criteria
                  </td>
                </tr>
              ) : (
                filteredIncidents.map((incident) => (
                  <tr
                    key={incident.incident_id}
                    className="hover:bg-slate-800/40 transition-colors group"
                  >
                    <td className="py-3.5 px-4 font-mono font-bold text-sky-400">
                      #{incident.incident_id}
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="font-medium text-slate-200">{incident.dataset}</div>
                      <div className="text-[11px] font-mono text-slate-400 truncate max-w-xs">
                        {incident.file_name}
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      <span className="font-mono text-[11px] bg-slate-800/80 px-2 py-0.5 rounded border border-slate-700/60">
                        {incident.incident_type}
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <Badge variant="severity" value={incident.severity}>
                        {incident.severity}
                      </Badge>
                    </td>
                    <td className="py-3.5 px-4">
                      <Badge variant="status" value={incident.status}>
                        {incident.status}
                      </Badge>
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-400 text-[11px] whitespace-nowrap">
                      {formatDate(incident.detected_at)}
                    </td>
                    <td className="py-3.5 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1.5">
                        <Button
                          variant="secondary"
                          size="sm"
                          icon={<Sparkles className="w-3.5 h-3.5 text-sky-400" />}
                          onClick={() => navigate(`/investigation?id=${incident.incident_id}`)}
                          title="Investigate with LangGraph + Bedrock"
                        >
                          Investigate
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          icon={<Wrench className="w-3.5 h-3.5 text-amber-400" />}
                          onClick={() => navigate(`/remediation?id=${incident.incident_id}`)}
                          title="Review Remediation Recommendation"
                        >
                          Remediation
                        </Button>
                      </div>
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
