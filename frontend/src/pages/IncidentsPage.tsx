import { useState, useEffect, useCallback } from 'react';
import { AlertOctagon, RefreshCw } from 'lucide-react';
import { getIncidents } from '../services/incidentService';
import { Incident } from '../types/api';
import { parseApiError } from '../services/api';
import { IncidentTable } from '../components/incidents/IncidentTable';
import { EmptyState } from '../components/ui/EmptyState';
import { Button } from '../components/ui/Button';
import { useGlobalRefresh } from '../components/layout/AppLayout';

export function IncidentsPage() {
  const { refreshCount } = useGlobalRefresh();
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchIncidents = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getIncidents();
      setIncidents(data);
    } catch (err: unknown) {
      const parsed = parseApiError(err);
      setError(parsed.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIncidents();
  }, [fetchIncidents, refreshCount]);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <AlertOctagon className="w-5 h-5 text-rose-400" />
            Incident Management & Triage
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time pipeline incidents detected across bronze landing, silver standardization, and gold aggregation layers.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-slate-400">
            Total Logged: <strong className="text-white font-bold">{incidents.length}</strong>
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchIncidents}
            isLoading={isLoading}
            icon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Refresh List
          </Button>
        </div>
      </div>

      {error ? (
        <EmptyState
          title="Failed to Load Incidents"
          description={error}
          variant="error"
          actionText="Retry"
          onAction={fetchIncidents}
        />
      ) : (
        <IncidentTable incidents={incidents} isLoading={isLoading} />
      )}
    </div>
  );
}
