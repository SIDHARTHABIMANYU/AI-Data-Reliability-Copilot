import { Sparkles, CheckCircle2, AlertTriangle, Layers, Cpu, ShieldCheck, ArrowRight } from 'lucide-react';
import { InvestigationResponse, IncidentEvidenceResponse } from '../../types/api';
import { Card, CardHeader, CardTitle } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

interface InvestigationViewProps {
  investigation: InvestigationResponse;
  evidencePackage?: IncidentEvidenceResponse | null;
  onNavigateRemediation: (incidentId: number) => void;
}

export function InvestigationView({
  investigation,
  evidencePackage,
  onNavigateRemediation,
}: InvestigationViewProps) {
  const getConfidenceBadge = (confidence: string) => {
    switch (confidence?.toUpperCase()) {
      case 'HIGH':
        return <Badge variant="success">CONFIDENCE: HIGH</Badge>;
      case 'MEDIUM':
        return <Badge variant="warning">CONFIDENCE: MEDIUM</Badge>;
      case 'LOW':
        return <Badge variant="danger">CONFIDENCE: LOW</Badge>;
      default:
        return <Badge variant="info">CONFIDENCE: {confidence}</Badge>;
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header Banner */}
      <div className="p-5 rounded-xl border border-sky-500/30 bg-gradient-to-r from-sky-950/40 via-slate-900/60 to-indigo-950/40 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">
              LANGGRAPH INVESTIGATION WORKFLOW
            </span>
            <span className="text-xs font-mono text-slate-400">
              Incident #{investigation.incident_id}
            </span>
          </div>
          <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            <Cpu className="w-5 h-5 text-sky-400" />
            AI Root Cause Analysis
          </h3>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl">
            Synthesized by Amazon Bedrock Claude with Pinecone RAG knowledge base & PostgreSQL telemetry.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {getConfidenceBadge(investigation.confidence)}
          <Button
            variant="primary"
            size="sm"
            onClick={() => onNavigateRemediation(investigation.incident_id)}
            icon={<ArrowRight className="w-3.5 h-3.5" />}
          >
            Review Remediation
          </Button>
        </div>
      </div>

      {/* Main Grid: Summary & Root Cause */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Executive Summary */}
        <Card className="border-slate-800">
          <CardHeader>
            <CardTitle>
              <Layers className="w-4 h-4 text-sky-400" />
              Incident Summary
            </CardTitle>
          </CardHeader>
          <div className="text-sm text-slate-200 leading-relaxed font-normal bg-slate-950/40 p-4 rounded-lg border border-slate-800/80">
            {investigation.summary || 'No summary provided by the investigation graph.'}
          </div>
        </Card>

        {/* Root Cause Card (Highlighted) */}
        <Card className="border-rose-900/40 bg-gradient-to-b from-rose-950/20 to-slate-900/60">
          <CardHeader>
            <CardTitle className="text-rose-300">
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              Diagnosed Root Cause
            </CardTitle>
            <span className="text-[10px] font-mono uppercase bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded border border-rose-500/30">
              Inferred Diagnosis
            </span>
          </CardHeader>
          <div className="text-sm text-rose-100 leading-relaxed p-4 rounded-lg bg-rose-950/30 border border-rose-800/40">
            {investigation.root_cause || 'Root cause could not be pinpointed.'}
          </div>
        </Card>
      </div>

      {/* Secondary Grid: Evidence & Business Impact */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Gathered Evidence List */}
        <Card>
          <CardHeader>
            <CardTitle>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Verified Telemetry Evidence ({investigation.evidence?.length || 0})
            </CardTitle>
            <span className="text-[10px] font-mono text-slate-400 uppercase">Factual Data</span>
          </CardHeader>
          <ul className="space-y-2.5">
            {investigation.evidence && investigation.evidence.length > 0 ? (
              investigation.evidence.map((item, idx) => (
                <li
                  key={idx}
                  className="text-xs text-slate-300 flex items-start gap-2.5 bg-slate-950/40 p-3 rounded-lg border border-slate-800/80"
                >
                  <span className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-mono font-bold flex items-center justify-center shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <span className="leading-relaxed">{item}</span>
                </li>
              ))
            ) : (
              <li className="text-xs text-slate-500 italic p-3">No specific evidence records listed.</li>
            )}
          </ul>
        </Card>

        {/* Impact Assessment */}
        <Card>
          <CardHeader>
            <CardTitle>
              <ShieldCheck className="w-4 h-4 text-amber-400" />
              Downstream & Business Impact ({investigation.impact?.length || 0})
            </CardTitle>
            <span className="text-[10px] font-mono text-slate-400 uppercase">Lineage Impact</span>
          </CardHeader>
          <ul className="space-y-2.5">
            {investigation.impact && investigation.impact.length > 0 ? (
              investigation.impact.map((item, idx) => (
                <li
                  key={idx}
                  className="text-xs text-amber-200/90 flex items-start gap-2.5 bg-amber-950/20 p-3 rounded-lg border border-amber-800/30"
                >
                  <span className="w-5 h-5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[10px] font-mono font-bold flex items-center justify-center shrink-0 mt-0.5">
                    !
                  </span>
                  <span className="leading-relaxed">{item}</span>
                </li>
              ))
            ) : (
              <li className="text-xs text-slate-500 italic p-3">No direct business impact recorded.</li>
            )}
          </ul>
        </Card>
      </div>

      {/* Recommended Action Callout */}
      <Card className="border-sky-500/30 bg-gradient-to-r from-sky-950/30 to-slate-900/60 p-5">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="text-[11px] font-mono uppercase tracking-wider text-sky-400 font-semibold flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" /> Recommended Remediation Action
            </div>
            <p className="text-sm font-medium text-slate-100 max-w-3xl leading-relaxed">
              {investigation.recommended_action || 'No recommendation generated.'}
            </p>
          </div>
          <Button
            variant="primary"
            onClick={() => onNavigateRemediation(investigation.incident_id)}
            className="shrink-0"
          >
            Go to Remediation Center
          </Button>
        </div>
      </Card>

      {/* Optional Raw Evidence Package Accordion */}
      {evidencePackage && (
        <Card className="border-slate-800/80 bg-slate-950/60">
          <CardHeader>
            <CardTitle>
              <Layers className="w-4 h-4 text-slate-400" />
              Source Telemetry Trace (GET /incidents/{investigation.incident_id}/evidence)
            </CardTitle>
            <span className="text-xs font-mono text-slate-500">Raw Pipeline Trace</span>
          </CardHeader>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            {evidencePackage.pipeline_run && (
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <div className="text-[10px] text-sky-400 uppercase font-semibold">Associated Pipeline Run</div>
                <div className="text-slate-300">Run ID: #{evidencePackage.pipeline_run.run_id}</div>
                <div className="text-slate-400">Dataset: {evidencePackage.pipeline_run.dataset}</div>
                <div className="text-slate-400">File: {evidencePackage.pipeline_run.file_name}</div>
                <div className="text-slate-400">Status: <Badge variant="status">{evidencePackage.pipeline_run.status}</Badge></div>
              </div>
            )}

            {evidencePackage.quality_results && evidencePackage.quality_results.length > 0 && (
              <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <div className="text-[10px] text-emerald-400 uppercase font-semibold">Data Quality Checks ({evidencePackage.quality_results.length})</div>
                <div className="max-h-28 overflow-y-auto space-y-1">
                  {evidencePackage.quality_results.map((q) => (
                    <div key={q.quality_id} className="text-[11px] text-slate-300 flex justify-between">
                      <span>{q.check_name}</span>
                      <Badge variant="status">{q.check_status}</Badge>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
}
