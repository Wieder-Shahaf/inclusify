import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

type Change = {
  value: number; // percentage, can be negative
  since: string;
};

export default function KpiCard({
  label,
  value,
  icon,
  change,
  accent = 'indigo',
  bgColor,
}: {
  label: string;
  value: string;
  icon?: ReactNode;
  change?: Change;
  accent?: 'indigo' | 'purple' | 'green' | 'amber' | 'rose' | 'sky';
  bgColor?: string;
}) {
  const up = (change?.value ?? 0) >= 0;
  const accentBg = {
    indigo: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-200',
    purple: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-200',
    green: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-200',
    amber: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-200',
    rose: 'bg-rose-100 text-rose-700 dark:bg-rose-900/30 dark:text-rose-200',
    sky: 'bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-200',
  }[accent];
  return (
    <div
      className="rounded-2xl border glass p-5 sm:p-6"
      style={bgColor ? { backgroundColor: bgColor } : undefined}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm text-slate-500 dark:text-slate-400">{label}</p>
          <p className="mt-2 text-3xl font-black tracking-tight">{value}</p>
        </div>
        {icon ? (
          <div className={cn('h-11 w-11 grid place-items-center rounded-xl', accentBg)}>
            {icon}
          </div>
        ) : null}
      </div>
      {change && (
        <p
          className={cn(
            'mt-3 text-sm font-medium',
            up ? 'text-green-600 dark:text-green-400' : 'text-rose-600 dark:text-rose-400'
          )}
        >
          {up ? '+' : ''}
          {change.value}% from {change.since}
        </p>
      )}
    </div>
  );
}
