'use client';

import { useTranslations } from 'next-intl';
import { cn } from '@/lib/utils';

export type Severity = 'outdated' | 'biased' | 'offensive' | 'incorrect';

export default function SeverityBadge({ level }: { level: Severity }) {
  const t = useTranslations('severity');
  const color = {
    outdated: 'bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-200',
    biased: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-200',
    offensive: 'bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-200',
    incorrect: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200',
  }[level];
  return <span className={cn('badge', color)}>{t(level)}</span>;
}
