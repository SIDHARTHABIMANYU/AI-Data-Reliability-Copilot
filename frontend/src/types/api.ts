export interface DashboardSummary {
  total_incidents: number;
  open_incidents: number;
  resolved_incidents: number;
  high_severity_incidents: number;
  pending_remediations: number;
  approved_remediations: number;
}

export type IncidentSeverity = 'HIGH' | 'MEDIUM' | 'LOW' | string;
export type IncidentStatus = 'OPEN' | 'RESOLVED' | 'INVESTIGATING' | string;

export interface Incident {
  incident_id: number;
  dataset: string;
  file_name: string;
  incident_type: string;
  severity: IncidentSeverity;
  description: string;
  status: IncidentStatus;
  detected_at: string;
  resolved_at: string | null;
}

export interface PipelineRunEvidence {
  run_id: number;
  dataset: string;
  file_name: string;
  run_date: string;
  row_count: number | null;
  status: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface QualityResultEvidence {
  quality_id: number;
  check_name: string;
  check_status: string;
  expected_value: string | null;
  actual_value: string | null;
  checked_at: string;
}

export interface IncidentEvidenceResponse {
  incident: Incident;
  pipeline_run: PipelineRunEvidence | null;
  quality_results: QualityResultEvidence[];
}

export interface InvestigationResponse {
  incident_id: number;
  summary: string;
  root_cause: string;
  evidence: string[];
  impact: string[];
  recommended_action: string;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface RemediationResponse {
  incident_id: number;
  remediation_id: number;
  problem: string;
  proposed_change: string;
  validation_steps: string[];
  risk: 'LOW' | 'MEDIUM' | 'HIGH';
  requires_approval: boolean;
}

export interface RemediationDecisionPayload {
  approved_by: string;
}

export interface RemediationDecisionResult {
  remediation_id: number;
  incident_id: number;
  status: 'APPROVED' | 'REJECTED' | string;
  approved_by?: string;
  approved_at?: string;
  rejected_by?: string;
  rejected_at?: string;
}

export interface AnomalyResult {
  anomaly_id: number;
  transaction_date: string;
  store_id: string;
  total_revenue: number | null;
  total_transactions: number;
  total_quantity: number;
  anomaly_score: number | null;
  anomaly_status: string;
  detection_method: string;
  detected_at: string;
}

export interface SystemHealth {
  status: string;
  isOnline: boolean;
  latencyMs?: number;
  lastChecked: Date;
  error?: string;
}

export interface ApiError {
  message: string;
  statusCode?: number;
  detail?: string;
}
