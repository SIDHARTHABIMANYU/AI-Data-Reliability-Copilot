import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Wrench, Search, Loader2 } from 'lucide-react';
import { getIncidentRemediation } from '../services/remediationService';
import { RemediationResponse } from '../types/api';
import { parseApiError } from '../services/api';
import { RemediationCard } from '../components/remediation/RemediationCard';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { EmptyState } from '../components/ui/EmptyState';
import { useToast } from '../hooks/useToast';

export function RemediationPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const toast = useToast();

  const queryId = searchParams.get('id');
  const [incidentIdInput, setIncidentIdInput] = useState(queryId || '1');
  const [activeIncidentId, setActiveIncidentId] = useState<number | null>(
    queryId ? parseInt(queryId, 10) : null
  );

  const [remediation, setRemediation] = useState<RemediationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchRemediation = useCallback(
    async (idToFetch: number) => {
      if (isNaN(idToFetch) || idToFetch < 1) {
        toast.error('Invalid ID', 'Please specify a valid numeric Incident ID.');
        return;
      }

      setIsLoading(true);
      setErrorMessage(null);
      setRemediation(null);

      try {
        const res = await getIncidentRemediation(idToFetch);
        setRemediation(res);
        toast.success(
          'Remediation Plan Loaded',
          `Plan #${res.remediation_id} ready for review.`
        );
      } catch (err: unknown) {
        const parsed = parseApiError(err);
        setErrorMessage(parsed.message);
        toast.error('Remediation Fetch Failed', parsed.message);
      } finally {
        setIsLoading(false);
      }
    },
    [toast]
  );

  useEffect(() => {
    if (queryId) {
      const parsed = parseInt(queryId, 10);
      if (!isNaN(parsed) && parsed > 0 && parsed !== activeIncidentId) {
        setActiveIncidentId(parsed);
        setIncidentIdInput(queryId);
        fetchRemediation(parsed);
      }
    }
  }, [queryId, fetchRemediation, activeIncidentId]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const parsed = parseInt(incidentIdInput.trim(), 10);
    if (!isNaN(parsed) && parsed > 0) {
      setSearchParams({ id: parsed.toString() });
      setActiveIncidentId(parsed);
      fetchRemediation(parsed);
    } else {
      toast.error('Invalid ID', 'Please enter a valid numeric Incident ID.');
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Wrench className="w-5 h-5 text-amber-400" />
            Remediation Center (Human-in-the-Loop)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Review AI proposed code/configuration adjustments, validate risk classification, and record operational approval.
          </p>
        </div>
      </div>

      {/* Input Bar */}
      <Card className="border-slate-800 bg-slate-900/80">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-end gap-3">
          <div className="w-full sm:w-64">
            <Input
              label="Incident ID"
              type="number"
              min="1"
              step="1"
              value={incidentIdInput}
              onChange={(e) => setIncidentIdInput(e.target.value)}
              placeholder="e.g. 1"
              disabled={isLoading}
            />
          </div>

          <Button
            type="submit"
            variant="primary"
            isLoading={isLoading}
            icon={<Wrench className="w-4 h-4" />}
            disabled={!incidentIdInput.trim()}
          >
            Fetch Remediation
          </Button>

          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/incidents')}
            disabled={isLoading}
          >
            Browse Incidents
          </Button>
        </form>
      </Card>

      {/* Loading */}
      {isLoading && (
        <Card className="border-amber-500/30 bg-amber-950/20 py-12 text-center flex flex-col items-center justify-center space-y-3">
          <Loader2 className="w-8 h-8 animate-spin text-amber-400" />
          <h4 className="text-sm font-semibold text-amber-200">
            Generating / Retrieving Remediation Recommendation...
          </h4>
          <p className="text-xs text-slate-400 max-w-md">
            Querying Bedrock AI for architectural validation steps and human approval requirements.
          </p>
        </Card>
      )}

      {/* Error */}
      {!isLoading && errorMessage && (
        <EmptyState
          title="Remediation Unavailable"
          description={errorMessage}
          variant="error"
          actionText="Retry Fetch"
          onAction={() => activeIncidentId && fetchRemediation(activeIncidentId)}
        />
      )}

      {/* Remediation Card */}
      {!isLoading && remediation && (
        <RemediationCard remediation={remediation} />
      )}

      {/* Empty Initial */}
      {!isLoading && !errorMessage && !remediation && (
        <EmptyState
          title="No Remediation Selected"
          description="Enter an incident ID above or select an incident from the Incident Management list to inspect the AI proposed remediation plan."
          icon={<Search className="w-10 h-10 text-amber-400" />}
          actionText="Browse Incidents"
          onAction={() => navigate('/incidents')}
        />
      )}
    </div>
  );
}
