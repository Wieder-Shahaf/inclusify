import { getTranslations } from 'next-intl/server';
import KpiCard from '@/components/dashboard/KpiCard';
import SimpleLineChart from '@/components/dashboard/SimpleLineChart';
import DonutChart from '@/components/dashboard/DonutChart';
import { paletteColor } from '@/lib/utils/palette';

export default async function AdminPage() {
  const t = await getTranslations();

  const kpis = [
    {
      label: t('admin.kpi.totalAnalyses'),
      value: '247',
      change: { value: 12, since: t('admin.kpi.since') },
      accent: 'sky' as const,
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M5 3h14a2 2 0 012 2v12a4 4 0 01-4 4H7a4 4 0 01-4-4V5a2 2 0 012-2zm2 4v2h10V7H7zm0 4v2h7v-2H7z" />
        </svg>
      ),
    },
    {
      label: t('admin.kpi.issuesFound'),
      value: '1,829',
      change: { value: -8, since: t('admin.kpi.since') },
      accent: 'amber' as const,
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M10.29 3.86l-8 14A1 1 0 003 19h16a1 1 0 00.86-1.5l-8-14a1 1 0 00-1.72 0zM12 9v4m0 4h.01" />
        </svg>
      ),
    },
    {
      label: t('admin.kpi.resolved'),
      value: '1,654',
      change: { value: 15, since: t('admin.kpi.since') },
      accent: 'green' as const,
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M9 12l2 2 4-5 2 2-6 7-4-4 2-2z" />
        </svg>
      ),
    },
    {
      label: t('admin.kpi.avgScore'),
      value: '82%',
      change: { value: 5, since: t('admin.kpi.since') },
      accent: 'purple' as const,
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
          <path d="M4 4h4v16H4V4zm6 6h4v10h-4V10zm6-4h4v14h-4V6z" />
        </svg>
      ),
    },
  ];

  const trendData = [68, 70, 69, 73, 76, 80, 77, 82, 81, 85, 84, 88];
  const trendLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  const issues = [
    { label: 'Outdated', value: 45, color: '#3b82f6' },
    { label: 'Biased', value: 30, color: '#f59e0b' },
    { label: 'Offensive', value: 15, color: '#ef4444' },
    { label: 'Incorrect', value: 10, color: '#8b5cf6' },
  ];

  const languages = [
    { lang: t('admin.languages.en'), runs: 142 },
    { lang: t('admin.languages.he'), runs: 95 },
  ];

  const topTerms = [
    { term: 'homosexual', count: 123, suggestion: 'gay/lesbian' },
    { term: 'sexual preference', count: 94, suggestion: 'sexual orientation' },
    { term: 'transsexual', count: 71, suggestion: 'transgender person' },
    { term: 'born as a man', count: 38, suggestion: 'assigned male at birth (AMAB)' },
  ];

  return (
    <div className="py-8">
      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        {kpis.map((k, i) => (
          <KpiCard
            key={i}
            label={k.label}
            value={k.value}
            change={k.change}
            accent={k.accent}
            icon={k.icon}
            bgColor={paletteColor(i)}
          />
        ))}
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <section
          className="xl:col-span-2 rounded-2xl border glass p-5 sm:p-6"
          style={{ backgroundColor: paletteColor(4) }}
        >
          <h3 className="text-lg font-semibold">{t('admin.scoreTrends')}</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400">{t('admin.avgOverTime')}</p>
          <div className="mt-4">
            <SimpleLineChart data={trendData} labels={trendLabels} color="#7b61ff" />
          </div>
        </section>
        <section
          className="rounded-2xl border glass p-5 sm:p-6"
          style={{ backgroundColor: paletteColor(1) }}
        >
          <h3 className="text-lg font-semibold">{t('admin.issuesBreakdown')}</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400">{t('admin.shareByCategory')}</p>
          <div className="mt-3 grid grid-cols-1 md:grid-cols-[1fr_auto] items-center gap-4">
            <div className="flex justify-center">
              <DonutChart
                data={issues}
                size={210}
                thickness={18}
                center={{
                  title: '1,829',
                  subtitle: t('admin.issuesFoundShort'),
                  titleClassName: 'text-lg sm:text-xl font-extrabold',
                  subtitleClassName: 'text-[10px] sm:text-xs text-slate-500 dark:text-slate-400',
                }}
              />
            </div>
            <div className="grid gap-2 text-sm md:pr-1">
              {issues.map((d, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span
                    className="h-3 w-3 rounded-full"
                    style={{ backgroundColor: d.color }}
                  ></span>
                  <span className="flex items-center gap-1 whitespace-nowrap">
                    <span>{d.label}</span>
                    <span className="font-semibold">{d.value}%</span>
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <section
          className="rounded-2xl border glass p-5 sm:p-6 lg:col-span-2"
          style={{ backgroundColor: paletteColor(2) }}
        >
          <h3 className="text-lg font-semibold">{t('admin.topTerms')}</h3>
          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500 dark:text-slate-400">
                  <th className="py-2 pr-4">{t('admin.table.term')}</th>
                  <th className="py-2 pr-4">{t('admin.table.occurrences')}</th>
                  <th className="py-2">{t('admin.table.suggestion')}</th>
                </tr>
              </thead>
              <tbody>
                {topTerms.map((r, i) => (
                  <tr
                    key={i}
                    className="border-t border-slate-200/60 dark:border-slate-800/60"
                  >
                    <td className="py-2 pr-4 font-medium">{r.term}</td>
                    <td className="py-2 pr-4">{r.count}</td>
                    <td className="py-2">{r.suggestion}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
        <section
          className="rounded-2xl border glass p-5 sm:p-6"
          style={{ backgroundColor: paletteColor(0) }}
        >
          <h3 className="text-lg font-semibold">{t('admin.usageByLanguage')}</h3>
          <div className="mt-4 grid gap-4">
            {languages.map((l, i) => (
              <div key={i}>
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">{l.lang}</span>
                  <span className="text-slate-500 dark:text-slate-400">
                    {l.runs} {t('admin.runs')}
                  </span>
                </div>
                <div className="mt-2 h-3 w-full rounded-full bg-slate-900/5 dark:bg-white/5 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-pride-purple to-pride-pink"
                    style={{ width: `${(l.runs / 200) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
