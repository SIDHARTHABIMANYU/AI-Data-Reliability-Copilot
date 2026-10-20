import { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  Layers,
} from 'lucide-react';
import { getIncidents, getIncidentEvidence } from '../services/incidentService';
import { Incident, QualityResultEvidence } from '../types/api';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { EmptyState } from '../components/ui/EmptyState';
import { formatDate } from '../lib/utils';
import { useGlobalRefresh } from '../components/layout/AppLayout';

export function DataQualityPage() {
  const navigate = useNavigate();
  const { refreshCount } = useGlobalRefresh();

  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [selectedIncidentId, setSelectedIncidentId] = useState<number | null>(null);
  const [qualityResults, setQualityResults] = useState<QualityResultEvidence[]>([]);
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLoadingEvidence, setIsLoadingEvidence] = useState(false);
  const [isLoadingIncidents, setIsLoadingIncidents] = useState(true);

  // Load incidents
  const loadIncidents = useCallback(async () => {
    setIsLoadingIncidents(true);
    try {
      const data = await getIncidents();
      setIncidents(data);
      if (data.length > 0 && selectedIncidentId === null) {
        setSelectedIncidentId(data[0].incident_id);
      }
    } catch {
      // Handled in UI
    } finally {
      setIsLoadingIncidents(false);
    }
  }, [selectedIncidentId]);

  useEffect(() => {
    loadIncidents();
  }, [loadIncidents, refreshCount]);

  // Load quality results for selected incident
  useEffect(() => {
    if (!selectedIncidentId) return;

    let isMounted = true;
    setIsLoadingEvidence(true);

    getIncidentEvidence(selectedIncidentId)
      .then((res) => {
        if (isMounted) {
          setQualityResults(res.quality_results || []);
        }
      })
      .catch(() => {
        if (isMounted) {
          setQualityResults([]);
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoadingEvidence(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [selectedIncidentId]);

  const filteredChecks = useMemo(() => {
    return qualityResults.filter((item) => {
      if (statusFilter === 'ALL') return true;
      return item.check_status.toUpperCase() === statusFilter;
    });
  }, [qualityResults, statusFilter]);

  const qualityRules = [
    {
      name: 'Schema & Null Integrity',
      check: 'Missing Values Detector',
      rule: 'Verifies critical columns (store_id, total_revenue) contain non-null, typed values.',
    },
    {
      name: 'Entity Uniqueness',
      check: 'Duplicate Record Detector',
      rule: 'Detects duplicate transaction keys across Bronze landing files before Silver ingestion.',
    },
    {
      name: 'Quarantine Routing',
      check: 'Contract Violation Quarantine',
      rule: 'Isolates malformed records into quarantine table without breaking downstream gold marts.',
    },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Data Quality & Contract Verification
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic data quality assertions, missing data identification, duplicate detection, and quarantine telemetry.
          </p>
        </div>
      </div>

      {/* Contract Rules Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {qualityRules.map((rule, idx) => (
          <Card key={idx} className="p-4 border border-slate-800 bg-slate-900/60">
            <div className="text-[10px] font-mono font-semibold uppercase text-sky-400 mb-1">
              {rule.check}
            </div>
            <h3 className="text-sm font-bold text-white mb-1">{rule.name}</h3>
            <p className="text-xs text-slate-400 leading-relaxed">{rule.rule}</p>
          </Card>
        ))}
      </div>

      {/* Incident-linked Quality Result Inspector */}
      <Card className="border-slate-800">
        <CardHeader>
          <CardTitle>
            <Layers className="w-4 h-4 text-emerald-400" />
            Verified Quality Results by Incident
          </CardTitle>
          <span className="text-xs font-mono text-slate-400">
            Source: <code>GET /incidents/{`{id}`}/evidence</code>
          </span>
        </CardHeader>

        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <label className="text-xs font-mono uppercase text-slate-400 shrink-0">
                Select Incident:
              </label>
              <select
                value={selectedIncidentId || ''}
                onChange={(e) => setSelectedIncidentId(parseInt(e.target.value, 10))}
                className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-sky-500"
                disabled={isLoadingIncidents || incidents.length === 0}
              >
                {incidents.map((inc) => (
                  <option key={inc.incident_id} value={inc.incident_id}>
                    Incident #{inc.incident_id} — {inc.dataset} ({inc.severity})
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-slate-400">Filter Status:</span>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200 focus:outline-none"
              >
                <option value="ALL">All Results</option>
                <option value="FAILED">Failed</option>
                <option value="PASSED">Passed</option>
              </select>
            </div>
          </div>

          {isLoadingEvidence ? (
            <div className="p-8 text-center text-xs font-mono text-slate-500">
              Loading quality verification checks from database...
            </div>
          ) : filteredChecks.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500 font-mono bg-slate-950/30 rounded-lg border border-slate-800">
              No quality check results found for this incident under current filter.
            </div>
          ) : (
            <div className="rounded-xl border border-slate-800 bg-slate-950/40 overflow-hidden">
              <table className="w-full text-left text-xs border-collapse font-mono">
                <thead>
                  <tr className="border-b border-slate-800 bg-slate-900/60 text-[10px] text-slate-400 uppercase tracking-wider">
                    <th className="py-2.5 px-3">Check ID</th>
                    <th className="py-2.5 px-3 font-sans">Check Name</th>
                    <th className="py-2.5 px-3">Status</th>
                    <th className="py-2.5 px-3">Expected Value</th>
                    <th className="py-2.5 px-3">Actual Value</th>
                    <th className="py-2.5 px-3">Timestamp</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-[11px]">
                  {filteredChecks.map((check) => (
                    <tr key={check.quality_id} className="hover:bg-slate-800/30">
                      <td className="py-2.5 px-3 text-sky-400 font-bold">
                        #{check.quality_id}
                      </td>
                      <td className="py-2.5 px-3 font-sans text-slate-200">
                        {check.check_name}
                      </td>
                      <td className="py-2.5 px-3">
                        <Badge variant="status" value={check.check_status}>
                          {check.check_status}
                        </Badge>
                      </td>
                      <td className="py-2.5 px-3 text-slate-400">
                        {check.expected_value || '—'}
                      </td>
                      <td className="py-2.5 px-3 text-slate-300">
                        {check.actual_value || '—'}
                      </td>
                      <td className="py-2.5 px-3 text-slate-500 text-[10px]">
                        {formatDate(check.checked_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Card>

      {/* Global Data Quality Feed Notice */}
      <EmptyState
        title="Global Quality Results Feed (REST Endpoint Pending)"
        description="Global background quality check records across all historical table scans are presently accessed via the MCP Server tool ('get_data_quality_results'). Dedicated REST endpoint adapter ('GET /data-quality') is scheduled for V12."
        variant="awaiting-integration"
        missingEndpoint="GET /data-quality"
        actionText="Triage Open Incidents"
        onAction={() => navigate('/incidents')}
      />
    </div>
  );
}
