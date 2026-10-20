import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return '—';
  try {
    const d = new Date(dateString);
    if (isNaN(d.getTime())) return dateString;
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    }).format(d);
  } catch {
    return dateString;
  }
}

export function formatNumber(val: number | null | undefined): string {
  if (val === null || val === undefined) return '—';
  return new Intl.NumberFormat('en-US').format(val);
}

export function formatCurrency(val: number | null | undefined): string {
  if (val === null || val === undefined) return '—';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2,
  }).format(val);
}

export function getSeverityBadgeClass(severity: string | undefined): string {
  switch (severity?.toUpperCase()) {
    case 'HIGH':
      return 'bg-red-500/15 text-red-400 border-red-500/30';
    case 'MEDIUM':
      return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
    case 'LOW':
      return 'bg-sky-500/15 text-sky-400 border-sky-500/30';
    default:
      return 'bg-slate-500/15 text-slate-300 border-slate-500/30';
  }
}

export function getStatusBadgeClass(status: string | undefined): string {
  switch (status?.toUpperCase()) {
    case 'OPEN':
      return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
    case 'RESOLVED':
    case 'APPROVED':
    case 'SUCCESS':
    case 'PASSED':
      return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
    case 'FAILED':
    case 'REJECTED':
    case 'ANOMALY':
      return 'bg-red-500/15 text-red-400 border-red-500/30';
    case 'PENDING':
    case 'INVESTIGATING':
    case 'RUNNING':
      return 'bg-blue-500/15 text-blue-400 border-blue-500/30';
    default:
      return 'bg-slate-500/15 text-slate-300 border-slate-500/30';
  }
}
