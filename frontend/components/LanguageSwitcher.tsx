'use client';

import { useLocale } from 'next-intl';
import { usePathname, useRouter } from 'next/navigation';
import { cn } from '@/lib/utils';

export default function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const switchLocale = (newLocale: string) => {
    let newPathname = pathname;
    // Handle locale in pathname
    if (pathname.startsWith(`/${locale}/`)) {
      newPathname = pathname.replace(`/${locale}/`, `/${newLocale}/`);
    } else if (pathname === `/${locale}`) {
      newPathname = `/${newLocale}`;
    } else if (pathname.startsWith('/')) {
      // If no locale prefix, add it
      newPathname = `/${newLocale}${pathname}`;
    }
    router.push(newPathname);
  };

  return (
    <div className="inline-flex rounded-lg border border-slate-200 dark:border-slate-800 overflow-hidden">
      <button
        onClick={() => switchLocale('en')}
        className={cn(
          'px-3 py-1 text-sm',
          locale === 'en' ? 'bg-slate-900/5 dark:bg-white/10' : ''
        )}
        aria-pressed={locale === 'en'}
      >
        EN
      </button>
      <button
        onClick={() => switchLocale('he')}
        className={cn(
          'px-3 py-1 text-sm',
          locale === 'he' ? 'bg-slate-900/5 dark:bg-white/10' : ''
        )}
        aria-pressed={locale === 'he'}
      >
        עברית
      </button>
    </div>
  );
}
