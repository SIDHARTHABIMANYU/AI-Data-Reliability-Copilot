import { useState, useEffect, useCallback, useMemo } from 'react';
import { ActivitySquare, RefreshCw, AlertTriangle, Store, Cpu } from 'lucide-react';
import { getAnomalies } from '../services/anomalyService';
import { AnomalyResult } from '../types/api';
import { parseApiError } from '../services/api';
import { AnomalyTable } from '../components/anomalies/AnomalyTable';
import { KPICard } from '../components/dashboard/KPICard';
import { EmptyState } from '../components/ui/EmptyState';
import { Button } from '../components/ui/Button';
import { useGlobalRefresh } from '../components/layout/AppLayout';

export function AnomalyDetectionPage() {
  const { refreshCount } = useGlobalRefresh();
  const [anomalies, setAnomalies] = useState<AnomalyResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnomalies = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAnomalies();
      setAnomalies(data);
    } catch (err: unknown) {
      const parsed = parseApiError(err);
      setError(parsed.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAnomalies();
  }, [fetchAnomalies, refreshCount]);

  const uniqueStores = useMemo(() => {
    const s = new Set<string>();
    anomalies.forEach((a) => a.store_id && s.add(a.store_id));
    return s.size;
  }, [anomalies]);

  const isolationForestCount = useMemo(() => {
    return anomalies.filter((a) => a.detection_method?.toLowerCase().includes('isolation')).length;
  }, [anomalies]);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <ActivitySquare className="w-5 h-5 text-amber-400" />
            Machine Learning Anomaly Detection
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Statistical rolling Z-scores and Scikit-learn Isolation Forest detections on store revenue, transactions, and volume.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={fetchAnomalies}
            isLoading={isLoading}
            icon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Refresh Anomalies
          </Button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <KPICard
          label="Total Anomalies"
          value={anomalies.length}
          icon={<AlertTriangle className="w-5 h-5" />}
          variant="warning"
          sublabel="Outliers detected in retail sales"
        />
        <KPICard
          label="Affected Stores"
          value={uniqueStores}
          icon={<Store className="w-5 h-5" />}
          variant="info"
          sublabel="Unique retail locations flagged"
        />
        <KPICard
          label="Isolation Forest Flagged"
          value={isolationForestCount}
          icon={<Cpu className="w-5 h-5" />}
          variant="danger"
          sublabel="Multivariate ML anomalies"
        />
      </div>

      {error ? (
        <EmptyState
          title="Failed to Load Anomalies"
          description={error}
          variant="error"
          actionText="Retry"
          onAction={fetchAnomalies}
        />
      ) : (
        <AnomalyTable anomalies={anomalies} isLoading={isLoading} />
      )}
    </div>
  );
}
