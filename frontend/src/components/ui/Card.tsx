import React from 'react';
import { cn } from '../../lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'glass-card rounded-xl border border-slate-800/80 bg-slate-900/60 p-5 shadow-sm text-slate-100',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className, ...props }: CardProps) {
  return (
    <div
      className={cn('flex items-center justify-between pb-3 border-b border-slate-800/60 mb-4', className)}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardTitle({ children, className, ...props }: CardProps) {
  return (
    <h3
      className={cn('text-sm font-semibold tracking-wide text-slate-200 uppercase flex items-center gap-2', className)}
      {...props}
    >
      {children}
    </h3>
  );
}
