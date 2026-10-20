import { apiClient } from './api';
import {
  Incident,
  IncidentEvidenceResponse,
  InvestigationResponse,
} from '../types/api';

export async function getIncidents(): Promise<Incident[]> {
  const res = await apiClient.get<Incident[]>('/incidents');
  return res.data;
}

export async function getIncidentEvidence(
  incidentId: number
): Promise<IncidentEvidenceResponse> {
  const res = await apiClient.get<IncidentEvidenceResponse>(
    `/incidents/${incidentId}/evidence`
  );
  return res.data;
}

export async function getIncidentInvestigation(
  incidentId: number
): Promise<InvestigationResponse> {
  // AI LangGraph workflow can take 15-45 seconds when invoking Bedrock
  const res = await apiClient.get<InvestigationResponse>(
    `/incidents/${incidentId}/investigation`,
    { timeout: 75000 }
  );
  return res.data;
}
