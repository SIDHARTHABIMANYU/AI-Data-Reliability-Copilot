import { apiClient } from './api';
import { DashboardSummary, SystemHealth } from '../types/api';

export async function checkSystemHealth(): Promise<SystemHealth> {
  const start = performance.now();
  try {
    const res = await apiClient.get<{ status: string }>('/health', { timeout: 5000 });
    const latencyMs = Math.round(performance.now() - start);
    return {
      status: res.data.status || 'healthy',
      isOnline: true,
      latencyMs,
      lastChecked: new Date(),
    };
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : 'Backend unreachable';
    return {
      status: 'offline',
      isOnline: false,
      lastChecked: new Date(),
      error: errorMsg,
    };
  }
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const res = await apiClient.get<DashboardSummary>('/dashboard/summary');
  return res.data;
}
