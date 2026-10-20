import { apiClient } from './api';
import {
  RemediationResponse,
  RemediationDecisionResult,
} from '../types/api';

export async function getIncidentRemediation(
  incidentId: number
): Promise<RemediationResponse> {
  const res = await apiClient.get<RemediationResponse>(
    `/incidents/${incidentId}/remediation`,
    { timeout: 75000 }
  );
  return res.data;
}

export async function approveRemediation(
  remediationId: number,
  approvedBy: string
): Promise<RemediationDecisionResult> {
  const res = await apiClient.post<RemediationDecisionResult>(
    `/remediations/${remediationId}/approve`,
    {
      approved_by: approvedBy.trim(),
    },
    { timeout: 30000 }
  );
  return res.data;
}

export async function rejectRemediation(
  remediationId: number,
  rejectedBy: string
): Promise<RemediationDecisionResult> {
  const res = await apiClient.post<RemediationDecisionResult>(
    `/remediations/${remediationId}/reject`,
    {
      approved_by: rejectedBy.trim(),
    },
    { timeout: 30000 }
  );
  return res.data;
}
