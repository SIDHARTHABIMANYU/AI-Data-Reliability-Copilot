import React from 'react';
import { Card } from '../ui/Card';
import { cn } from '../../lib/utils';

interface KPICardProps {
  label: string;
  value: number | string | undefined;
  icon: React.ReactNode;
  variant?: 'default' | 'danger' | 'warning' | 'success' | 'info';
  sublabel?: string;
  className?: string;
}

export function KPICard({
  label,
  value,
  icon,
  variant = 'default',
  sublabel,
  className,
}: KPICardProps) {
  const variantStyles = {
    default: 'text-slate-100 border-slate-800 bg-slate-900/60',
    danger: 'text-rose-400 border-rose-900/40 bg-rose-950/20',
    warning: 'text-amber-400 border-amber-900/40 bg-amber-950/20',
    success: 'text-emerald-400 border-emerald-900/40 bg-emerald-950/20',
    info: 'text-sky-400 border-sky-900/40 bg-sky-950/20',
  };

  const iconBgStyles = {
    default: 'bg-slate-800 text-slate-300',
    danger: 'bg-rose-500/15 text-rose-400 border border-rose-500/30',
    warning: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
    success: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30',
    info: 'bg-sky-500/15 text-sky-400 border border-sky-500/30',
  };

  return (
    <Card
      className={cn(
        'glass-card glass-card-hover p-4 md:p-5 flex flex-col justify-between border transition-all',
        variantStyles[variant],
        className
      )}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {label}
        </span>
        <div className={cn('p-2 rounded-lg', iconBgStyles[variant])}>{icon}</div>
      </div>

      <div>
        <div className="text-2xl md:text-3xl font-bold font-mono tracking-tight text-white">
          {value !== undefined ? value : '—'}
        </div>
        {sublabel && (
          <p className="mt-1 text-xs text-slate-400 font-normal">{sublabel}</p>
        )}
      </div>
    </Card>
  );
}
