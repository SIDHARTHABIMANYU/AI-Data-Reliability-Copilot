import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  GitMerge,
  Database,
  Sparkles,
} from 'lucide-react';
import { getIncidents, getIncidentEvidence } from '../services/incidentService';
import { Incident, PipelineRunEvidence } from '../types/api';
import { Card, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { EmptyState } from '../components/ui/EmptyState';
import { formatDate } from '../lib/utils';
import { useGlobalRefresh } from '../components/layout/AppLayout';

export function PipelineMonitoringPage() {
  const navigate = useNavigate();
  const { refreshCount } = useGlobalRefresh();

  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [selectedIncidentId, setSelectedIncidentId] = useState<number | null>(null);
  const [pipelineRun, setPipelineRun] = useState<PipelineRunEvidence | null>(null);
  const [isLoadingEvidence, setIsLoadingEvidence] = useState(false);
  const [isLoadingIncidents, setIsLoadingIncidents] = useState(true);

  // Load available incidents to allow inspection of linked pipeline runs
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

  // Load pipeline run evidence for selected incident
  useEffect(() => {
    if (!selectedIncidentId) return;

    let isMounted = true;
    setIsLoadingEvidence(true);

    getIncidentEvidence(selectedIncidentId)
      .then((res) => {
        if (isMounted) {
          setPipelineRun(res.pipeline_run);
        }
      })
      .catch(() => {
        if (isMounted) {
          setPipelineRun(null);
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

  const stages = [
    {
      name: 'Bronze Layer',
      badge: 'RAW S3 INGESTION',
      desc: 'Raw CSV retail landing in AWS S3 buckets (sales, inventory, suppliers).',
      tech: 'AWS S3 • Boto3 • Ingestion Service',
      color: 'border-amber-700/40 bg-amber-950/20 text-amber-300',
    },
    {
      name: 'Silver Layer',
      badge: 'STANDARDIZATION & QUALITY',
      desc: 'Pandas schema validation, missing data imputation, duplicate deduplication, and quarantine.',
      tech: 'Pandas • Great Expectations • Quarantine DB',
      color: 'border-slate-600/40 bg-slate-900/40 text-slate-300',
    },
    {
      name: 'Gold Layer',
      badge: 'BUSINESS ANALYTICS',
      desc: 'Aggregated store metrics, daily revenue rollups, and anomaly detection feeds.',
      tech: 'PostgreSQL • Scikit-Learn • Bedrock RAG',
      color: 'border-yellow-600/40 bg-yellow-950/20 text-yellow-300',
    },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <GitMerge className="w-5 h-5 text-sky-400" />
            Medallion Pipeline Execution
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            End-to-end telemetry across Bronze S3 ingestion, Silver standardization, and Gold business marts.
          </p>
        </div>
      </div>

      {/* Medallion Pipeline Stage Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {stages.map((stage, idx) => (
          <Card key={idx} className={`p-4 border ${stage.color} flex flex-col justify-between`}>
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono font-bold tracking-wider px-2 py-0.5 rounded bg-black/40 border border-current">
                  {stage.badge}
                </span>
                <span className="text-xs font-mono opacity-60">Stage {idx + 1}</span>
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">{stage.name}</h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-3">{stage.desc}</p>
            </div>
            <div className="pt-2 border-t border-slate-800/60 text-[11px] font-mono text-slate-500">
              {stage.tech}
            </div>
          </Card>
        ))}
      </div>

      {/* Incident-linked Pipeline Run Inspector */}
      <Card className="border-slate-800">
        <CardHeader>
          <CardTitle>
            <Database className="w-4 h-4 text-sky-400" />
            Incident-Linked Pipeline Run Inspector
          </CardTitle>
          <span className="text-xs font-mono text-slate-400">
            Source: <code>GET /incidents/{`{id}`}/evidence</code>
          </span>
        </CardHeader>

        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
            <label className="text-xs font-mono uppercase text-slate-400 shrink-0">
              Select Incident to Inspect Run:
            </label>
            <select
              value={selectedIncidentId || ''}
              onChange={(e) => setSelectedIncidentId(parseInt(e.target.value, 10))}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-sky-500"
              disabled={isLoadingIncidents || incidents.length === 0}
            >
              {incidents.map((inc) => (
                <option key={inc.incident_id} value={inc.incident_id}>
                  Incident #{inc.incident_id} — {inc.dataset} ({inc.incident_type})
                </option>
              ))}
            </select>
          </div>

          {isLoadingEvidence ? (
            <div className="p-8 text-center text-xs font-mono text-slate-500">
              Fetching pipeline execution telemetry from evidence service...
            </div>
          ) : pipelineRun ? (
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold font-mono text-sky-400">
                    Run #{pipelineRun.run_id}
                  </span>
                  <Badge variant="status" value={pipelineRun.status}>
                    {pipelineRun.status}
                  </Badge>
                </div>
                <div className="text-xs font-mono text-slate-400">
                  Target: <strong className="text-slate-200">{pipelineRun.dataset}</strong> /{' '}
                  <span className="text-slate-300">{pipelineRun.file_name}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono pt-1">
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Row Count</span>
                  <span className="text-slate-200 font-bold">
                    {pipelineRun.row_count !== null ? pipelineRun.row_count.toLocaleString() : '—'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Run Date</span>
                  <span className="text-slate-200">{pipelineRun.run_date || '—'}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Started At</span>
                  <span className="text-slate-200">{formatDate(pipelineRun.started_at)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Completed At</span>
                  <span className="text-slate-200">{formatDate(pipelineRun.completed_at)}</span>
                </div>
              </div>

              <div className="pt-2 flex justify-end">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate(`/investigation?id=${selectedIncidentId}`)}
                  icon={<Sparkles className="w-3.5 h-3.5" />}
                >
                  Investigate Linked Incident #{selectedIncidentId}
                </Button>
              </div>
            </div>
          ) : (
            <div className="p-6 text-center text-xs text-slate-500 font-mono bg-slate-950/30 rounded-lg border border-slate-800/60">
              No specific pipeline run record linked to this incident in the evidence store.
            </div>
          )}
        </div>
      </Card>

      {/* Global Pipeline Run History Endpoint Status Notice */}
      <EmptyState
        title="Global Pipeline Batch History (REST Endpoint Pending)"
        description="Global background execution logs across un-alerted pipeline runs are currently queried via the MCP Server tool ('get_pipeline_runs'). In compliance with architecture requirements, browser clients do not speak raw MCP protocol directly. A dedicated FastAPI adapter endpoint is scheduled for V12."
        variant="awaiting-integration"
        missingEndpoint="GET /pipelines/runs"
        actionText="View Incident Telemetry"
        onAction={() => navigate('/incidents')}
      />
    </div>
  );
}
