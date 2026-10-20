import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  GitMerge,
  ShieldCheck,
  ActivitySquare,
  AlertOctagon,
  Sparkles,
  Wrench,
  Server,
  CheckCircle2,
  XCircle,
  Wifi,
} from 'lucide-react';
import { SystemHealth } from '../../types/api';
import { cn } from '../../lib/utils';

interface SidebarProps {
  health: SystemHealth | null;
  isOpen: boolean;
  onCloseMobile: () => void;
}

const navItems = [
  { name: 'Overview', to: '/', icon: LayoutDashboard },
  { name: 'Pipeline Monitoring', to: '/pipelines', icon: GitMerge },
  { name: 'Data Quality', to: '/quality', icon: ShieldCheck },
  { name: 'Anomaly Detection', to: '/anomalies', icon: ActivitySquare },
  { name: 'Incidents', to: '/incidents', icon: AlertOctagon },
  { name: 'AI Investigation', to: '/investigation', icon: Sparkles },
  { name: 'Remediation Center', to: '/remediation', icon: Wrench },
];

export function Sidebar({ health, isOpen, onCloseMobile }: SidebarProps) {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={cn(
          'fixed top-0 bottom-0 left-0 z-40 w-64 bg-[#080d16] border-r border-slate-800/80 flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Brand / Logo */}
        <div className="h-16 px-5 flex items-center gap-3 border-b border-slate-800/80">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center shadow-md shadow-sky-500/20 shrink-0">
            <Sparkles className="w-5 h-5 text-slate-950" />
          </div>
          <div className="min-w-0">
            <h1 className="text-sm font-bold tracking-tight text-white leading-tight truncate">
              Reliability Copilot
            </h1>
            <p className="text-[11px] font-mono tracking-wider text-sky-400">
              V11 ENTERPRISE
            </p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
            Observability & Ops
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === '/'}
                onClick={onCloseMobile}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all group',
                    isActive
                      ? 'bg-sky-500/15 text-sky-400 border border-sky-500/30 font-semibold shadow-sm shadow-sky-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  )
                }
              >
                <Icon className="w-4 h-4 shrink-0 transition-colors group-hover:text-slate-200" />
                <span className="truncate">{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* System Status Section */}
        <div className="p-3 border-t border-slate-800/80 bg-[#06090e]/60">
          <div className="p-3 rounded-lg border border-slate-800 bg-slate-900/60">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Server className="w-3.5 h-3.5 text-slate-400" />
                Backend Node
              </span>
              {health?.isOnline ? (
                <span className="inline-flex items-center gap-1 text-[10px] text-emerald-400 font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Live
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-[10px] text-rose-400 font-medium">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
                  Offline
                </span>
              )}
            </div>

            <div className="text-xs font-mono text-slate-300 truncate mb-1">
              {import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-400">
              <span className="flex items-center gap-1">
                <Wifi className="w-3 h-3" />
                {health?.latencyMs !== undefined ? `${health.latencyMs}ms` : '—'}
              </span>
              <span>
                {health?.isOnline ? (
                  <span className="text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" /> FastAPI 1.0
                  </span>
                ) : (
                  <span className="text-rose-400 flex items-center gap-1">
                    <XCircle className="w-3 h-3" /> Disconnected
                  </span>
                )}
              </span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
