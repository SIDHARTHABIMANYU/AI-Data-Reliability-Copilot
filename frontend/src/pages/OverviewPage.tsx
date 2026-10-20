import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AlertOctagon,
  AlertTriangle,
  Clock,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import { getDashboardSummary } from '../services/dashboardService';
import { getIncidents } from '../services/incidentService';
import { DashboardSummary, Incident } from '../types/api';
import { parseApiError } from '../services/api';
import { KPICard } from '../components/dashboard/KPICard';
import { SeverityChart } from '../components/dashboard/SeverityChart';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { EmptyState } from '../components/ui/EmptyState';
import { Skeleton } from '../components/ui/Skeleton';
import { formatDate } from '../lib/utils';
import { useGlobalRefresh } from '../components/layout/AppLayout';

export function OverviewPage() {
  const navigate = useNavigate();
  const { refreshCount } = useGlobalRefresh();

  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const [summaryRes, incidentsRes] = await Promise.all([
        getDashboardSummary(),
        getIncidents().catch(() => [] as Incident[]),
      ]);
      setSummary(summaryRes);
      setIncidents(incidentsRes);
    } catch (err: unknown) {
      const parsed = parseApiError(err);
      setErrorMessage(parsed.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData, refreshCount]);

  if (errorMessage && !summary) {
    return (
      <div className="py-8">
        <EmptyState
          title="Backend Unreachable"
          description={errorMessage}
          variant="error"
          actionText="Retry Connection"
          onAction={loadData}
        />
      </div>
    );
  }

  const recentIncidents = incidents.slice(0, 5);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Platform Banner */}
      <div className="p-5 rounded-xl border border-slate-800 bg-gradient-to-r from-slate-900/90 via-[#0b1322]/80 to-slate-900/90 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-sky-500/10 border border-sky-500/20 text-[11px] font-mono text-sky-400 mb-2">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-pulse" />
            LIVE TELEMETRY STREAM
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            Data Reliability & Incident Command
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Autonomous anomaly monitoring, LangGraph multi-step investigation, and human-in-the-loop remediation across retail medallion pipelines.
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate('/investigation')}
            icon={<Sparkles className="w-4 h-4" />}
          >
            Launch Investigation
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/incidents')}
          >
            View All Incidents
          </Button>
        </div>
      </div>

      {/* Primary KPI Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {isLoading ? (
          <>
            <Skeleton className="h-28" />
            <Skeleton className="h-28" />
            <Skeleton className="h-28" />
            <Skeleton className="h-28" />
          </>
        ) : (
          <>
            <KPICard
              label="Total Incidents"
              value={summary?.total_incidents}
              icon={<AlertOctagon className="w-5 h-5" />}
              variant="default"
              sublabel="All detected incidents"
            />
            <KPICard
              label="Open Incidents"
              value={summary?.open_incidents}
              icon={<AlertTriangle className="w-5 h-5" />}
              variant="warning"
              sublabel="Active requiring attention"
            />
            <KPICard
              label="High Severity"
              value={summary?.high_severity_incidents}
              icon={<AlertOctagon className="w-5 h-5" />}
              variant="danger"
              sublabel="Critical pipeline blockers"
            />
            <KPICard
              label="Pending Remediations"
              value={summary?.pending_remediations}
              icon={<Clock className="w-5 h-5" />}
              variant="info"
              sublabel="Awaiting human approval"
            />
          </>
        )}
      </div>

      {/* Middle Section: Distribution Chart & System Highlights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Severity Chart */}
        <div className="lg:col-span-1">
          {isLoading ? (
            <Skeleton className="h-80" />
          ) : (
            <SeverityChart
              highCount={summary?.high_severity_incidents || 0}
              openCount={summary?.open_incidents || 0}
              resolvedCount={summary?.resolved_incidents || 0}
              totalCount={summary?.total_incidents || 0}
            />
          )}
        </div>

        {/* Recent Incidents Card */}
        <div className="lg:col-span-2">
          <Card className="h-full flex flex-col justify-between">
            <div>
              <CardHeader>
                <CardTitle>
                  <AlertOctagon className="w-4 h-4 text-sky-400" />
                  Recent Detected Incidents
                </CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate('/incidents')}
                  icon={<ArrowRight className="w-3.5 h-3.5" />}
                >
                  View All ({incidents.length})
                </Button>
              </CardHeader>

              {isLoading ? (
                <div className="space-y-3 py-2">
                  <Skeleton className="h-10" />
                  <Skeleton className="h-10" />
                  <Skeleton className="h-10" />
                </div>
              ) : recentIncidents.length === 0 ? (
                <div className="py-12 text-center text-xs text-slate-500 font-mono">
                  No active incidents recorded in database.
                </div>
              ) : (
                <div className="divide-y divide-slate-800/60 overflow-x-auto">
                  {recentIncidents.map((incident) => (
                    <div
                      key={incident.incident_id}
                      className="py-3 px-1 flex items-center justify-between gap-4 hover:bg-slate-800/30 rounded-lg transition-colors"
                    >
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-sky-400">
                            #{incident.incident_id}
                          </span>
                          <span className="text-xs font-semibold text-slate-200 truncate">
                            {incident.dataset}
                          </span>
                          <Badge variant="severity" value={incident.severity}>
                            {incident.severity}
                          </Badge>
                          <Badge variant="status" value={incident.status}>
                            {incident.status}
                          </Badge>
                        </div>
                        <p className="text-[11px] text-slate-400 truncate mt-0.5">
                          {incident.description}
                        </p>
                      </div>

                      <div className="flex items-center gap-3 shrink-0">
                        <span className="hidden sm:inline text-[11px] font-mono text-slate-400">
                          {formatDate(incident.detected_at)}
                        </span>
                        <Button
                          variant="secondary"
                          size="sm"
                          onClick={() => navigate(`/investigation?id=${incident.incident_id}`)}
                        >
                          Investigate
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Bottom mini-summary */}
            <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                {summary?.resolved_incidents || 0} Resolved incidents in history
              </span>
              <span className="flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />
                {summary?.approved_remediations || 0} Remediations approved
              </span>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
