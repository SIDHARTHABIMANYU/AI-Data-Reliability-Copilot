import { apiClient } from './api';
import { AnomalyResult } from '../types/api';

export async function getAnomalies(): Promise<AnomalyResult[]> {
  const res = await apiClient.get<AnomalyResult[]>('/anomalies');
  return res.data;
}
