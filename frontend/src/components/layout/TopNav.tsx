import { useLocation } from 'react-router-dom';
import { Menu, RefreshCw, AlertCircle, CheckCircle2, ShieldAlert } from 'lucide-react';
import { SystemHealth } from '../../types/api';
import { Button } from '../ui/Button';

interface TopNavProps {
  health: SystemHealth | null;
  lastRefreshed: Date | null;
  isRefreshing: boolean;
  onRefresh: () => void;
  onOpenMobileMenu: () => void;
  error?: string | null;
}

const pageTitles: Record<string, { title: string; category: string }> = {
  '/': { title: 'Platform Reliability Overview', category: 'Observability' },
  '/pipelines': { title: 'Pipeline Medallion Execution', category: 'Data Engineering' },
  '/quality': { title: 'Data Quality & Contracts', category: 'Data Governance' },
  '/anomalies': { title: 'Retail ML Anomaly Detection', category: 'Machine Learning' },
  '/incidents': { title: 'Incident Management & Triage', category: 'Reliability Ops' },
  '/investigation': { title: 'AI Copilot Investigation', category: 'Agentic AI' },
  '/remediation': { title: 'Remediation Review Center', category: 'Human-in-the-Loop' },
};

export function TopNav({
  health,
  lastRefreshed,
  isRefreshing,
  onRefresh,
  onOpenMobileMenu,
  error,
}: TopNavProps) {
  const location = useLocation();
  const current = pageTitles[location.pathname] || {
    title: 'Data Reliability Copilot',
    category: 'Enterprise',
  };

  const formattedTime = lastRefreshed
    ? new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      }).format(lastRefreshed)
    : 'Never';

  return (
    <header className="sticky top-0 z-30 h-16 bg-[#080d16]/90 backdrop-blur-md border-b border-slate-800/80 px-4 sm:px-6 flex items-center justify-between">
      {/* Left: Mobile hamburger & Breadcrumbs */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMobileMenu}
          className="lg:hidden p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
          aria-label="Open sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <div className="flex items-center gap-2 text-[11px] font-mono text-slate-400 tracking-wider uppercase">
            <span>AI Copilot</span>
            <span>/</span>
            <span className="text-sky-400">{current.category}</span>
          </div>
          <h2 className="text-base font-semibold text-white tracking-tight">
            {current.title}
          </h2>
        </div>
      </div>

      {/* Right: Refresh button, Last updated, Error badge */}
      <div className="flex items-center gap-3">
        {/* Global Error Banner pill if error */}
        {error && (
          <div className="hidden md:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-xs text-rose-400">
            <ShieldAlert className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate max-w-xs">{error}</span>
          </div>
        )}

        {/* Backend connectivity indicator */}
        <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-lg border border-slate-800 bg-slate-900/60 text-xs font-mono">
          {health?.isOnline ? (
            <span className="text-emerald-400 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>API Connected</span>
            </span>
          ) : (
            <span className="text-rose-400 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5" />
              <span>API Offline</span>
            </span>
          )}
        </div>

        {/* Last Refreshed Timestamp */}
        <div className="hidden lg:flex flex-col text-right">
          <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400">
            Last Synced
          </span>
          <span className="text-xs font-mono text-slate-300">{formattedTime}</span>
        </div>

        {/* Refresh Action */}
        <Button
          variant="secondary"
          size="sm"
          onClick={onRefresh}
          isLoading={isRefreshing}
          icon={<RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />}
          title="Refresh dashboard data"
        >
          <span className="hidden sm:inline">Sync</span>
        </Button>
      </div>
    </header>
  );
}
