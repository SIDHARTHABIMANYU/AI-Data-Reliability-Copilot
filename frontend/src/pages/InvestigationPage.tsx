import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Sparkles, Search, Loader2 } from 'lucide-react';
import { getIncidentInvestigation, getIncidentEvidence } from '../services/incidentService';
import { InvestigationResponse, IncidentEvidenceResponse } from '../types/api';
import { parseApiError } from '../services/api';
import { InvestigationView } from '../components/investigation/InvestigationView';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { EmptyState } from '../components/ui/EmptyState';
import { useToast } from '../hooks/useToast';

export function InvestigationPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const toast = useToast();

  const queryId = searchParams.get('id');
  const [incidentIdInput, setIncidentIdInput] = useState(queryId || '1');
  const [activeIncidentId, setActiveIncidentId] = useState<number | null>(
    queryId ? parseInt(queryId, 10) : null
  );

  const [investigation, setInvestigation] = useState<InvestigationResponse | null>(null);
  const [evidencePackage, setEvidencePackage] = useState<IncidentEvidenceResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const runInvestigation = useCallback(
    async (idToRun: number) => {
      if (isNaN(idToRun) || idToRun < 1) {
        toast.error('Invalid ID', 'Please specify a valid numeric Incident ID.');
        return;
      }

      setIsLoading(true);
      setErrorMessage(null);
      setInvestigation(null);
      setEvidencePackage(null);

      try {
        // Run AI investigation and parallel evidence fetch
        const [invRes, evRes] = await Promise.all([
          getIncidentInvestigation(idToRun),
          getIncidentEvidence(idToRun).catch(() => null),
        ]);

        setInvestigation(invRes);
        setEvidencePackage(evRes);
        toast.success(
          'Investigation Complete',
          `LangGraph synthesized incident #${idToRun} with ${invRes.confidence} confidence.`
        );
      } catch (err: unknown) {
        const parsed = parseApiError(err);
        setErrorMessage(parsed.message);
        toast.error('Investigation Failed', parsed.message);
      } finally {
        setIsLoading(false);
      }
    },
    [toast]
  );

  // Trigger automatically if navigated with ?id=
  useEffect(() => {
    if (queryId) {
      const parsed = parseInt(queryId, 10);
      if (!isNaN(parsed) && parsed > 0 && parsed !== activeIncidentId) {
        setActiveIncidentId(parsed);
        setIncidentIdInput(queryId);
        runInvestigation(parsed);
      }
    }
  }, [queryId, runInvestigation, activeIncidentId]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const parsed = parseInt(incidentIdInput.trim(), 10);
    if (!isNaN(parsed) && parsed > 0) {
      setSearchParams({ id: parsed.toString() });
      setActiveIncidentId(parsed);
      runInvestigation(parsed);
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
            <Sparkles className="w-5 h-5 text-sky-400" />
            AI Incident Investigation (LangGraph + Bedrock)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Autonomous multi-agent workflow analyzing pipeline runs, data quality check results, and Pinecone RAG vectors.
          </p>
        </div>
      </div>

      {/* Incident Input Bar */}
      <Card className="border-slate-800 bg-slate-900/80">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-end gap-3">
          <div className="w-full sm:w-64">
            <Input
              label="Incident ID to Investigate"
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
            icon={<Sparkles className="w-4 h-4" />}
            disabled={!incidentIdInput.trim()}
          >
            Investigate Incident
          </Button>

          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/incidents')}
            disabled={isLoading}
          >
            Select From Incidents
          </Button>
        </form>
      </Card>

      {/* Loading feedback */}
      {isLoading && (
        <Card className="border-sky-500/30 bg-sky-950/20 py-12 text-center flex flex-col items-center justify-center space-y-3">
          <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
          <h4 className="text-sm font-semibold text-sky-200">
            Running LangGraph Reliability Copilot Workflow...
          </h4>
          <p className="text-xs text-slate-400 max-w-md">
            Querying PostgreSQL telemetry, executing Pinecone RAG semantic search, and streaming analysis via AWS Bedrock Claude. This typically takes 15–30 seconds.
          </p>
        </Card>
      )}

      {/* Error state */}
      {!isLoading && errorMessage && (
        <EmptyState
          title="Investigation Could Not Complete"
          description={errorMessage}
          variant="error"
          actionText="Retry Investigation"
          onAction={() => activeIncidentId && runInvestigation(activeIncidentId)}
        />
      )}

      {/* Result view */}
      {!isLoading && investigation && (
        <InvestigationView
          investigation={investigation}
          evidencePackage={evidencePackage}
          onNavigateRemediation={(id) => navigate(`/remediation?id=${id}`)}
        />
      )}

      {/* Initial state before search */}
      {!isLoading && !errorMessage && !investigation && (
        <EmptyState
          title="Ready to Investigate"
          description="Enter an incident ID above or choose an incident from the Incident Management table to initiate automated root-cause analysis."
          icon={<Search className="w-10 h-10 text-sky-400" />}
          actionText="Browse Incidents"
          onAction={() => navigate('/incidents')}
        />
      )}
    </div>
  );
}
