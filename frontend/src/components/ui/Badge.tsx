import { cn, getSeverityBadgeClass, getStatusBadgeClass } from '../../lib/utils';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'severity' | 'status' | 'default' | 'outline' | 'info' | 'success' | 'warning' | 'danger';
  value?: string;
  className?: string;
}

export function Badge({ children, variant = 'default', value, className }: BadgeProps) {
  let badgeStyle = 'bg-slate-800 text-slate-300 border-slate-700/60';

  if (variant === 'severity') {
    badgeStyle = getSeverityBadgeClass(value || String(children));
  } else if (variant === 'status') {
    badgeStyle = getStatusBadgeClass(value || String(children));
  } else if (variant === 'info') {
    badgeStyle = 'bg-sky-500/15 text-sky-400 border-sky-500/30';
  } else if (variant === 'success') {
    badgeStyle = 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
  } else if (variant === 'warning') {
    badgeStyle = 'bg-amber-500/15 text-amber-400 border-amber-500/30';
  } else if (variant === 'danger') {
    badgeStyle = 'bg-rose-500/15 text-rose-400 border-rose-500/30';
  } else if (variant === 'outline') {
    badgeStyle = 'bg-transparent text-slate-400 border-slate-700';
  }

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border tracking-wider',
        badgeStyle,
        className
      )}
    >
      {children}
    </span>
  );
}
