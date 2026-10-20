import React from 'react';
import { AlertCircle, HelpCircle, ServerCrash } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  actionText?: string;
  onAction?: () => void;
  missingEndpoint?: string;
  variant?: 'default' | 'error' | 'awaiting-integration' | 'info';
  className?: string;
}

export function EmptyState({
  title,
  description,
  icon,
  actionText,
  onAction,
  missingEndpoint,
  variant = 'default',
  className,
}: EmptyStateProps) {
  const getIcon = () => {
    if (icon) return icon;
    if (variant === 'error') return <ServerCrash className="w-10 h-10 text-rose-400" />;
    if (variant === 'awaiting-integration') return <AlertCircle className="w-10 h-10 text-amber-400" />;
    return <HelpCircle className="w-10 h-10 text-slate-500" />;
  };

  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center text-center p-8 md:p-12 rounded-xl border border-dashed border-slate-800 bg-slate-900/40',
        variant === 'error' && 'border-rose-900/40 bg-rose-950/10',
        variant === 'awaiting-integration' && 'border-amber-900/40 bg-amber-950/10',
        className
      )}
    >
      <div className="p-3 rounded-full bg-slate-800/80 mb-4 inline-flex items-center justify-center border border-slate-700/60 shadow-inner">
        {getIcon()}
      </div>

      <h4 className="text-base font-semibold text-slate-200 mb-2">{title}</h4>
      <p className="text-sm text-slate-400 max-w-md mb-4 leading-relaxed">{description}</p>

      {missingEndpoint && (
        <div className="mb-5 inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-amber-500/10 border border-amber-500/20 text-xs font-mono text-amber-300">
          <span className="font-sans uppercase text-[10px] tracking-wider bg-amber-500/20 px-1 py-0.5 rounded text-amber-200">
            Backend Gap
          </span>
          <code>{missingEndpoint}</code>
        </div>
      )}

      {actionText && onAction && (
        <Button variant="outline" size="sm" onClick={onAction}>
          {actionText}
        </Button>
      )}
    </div>
  );
}
