import { useTranslations } from 'next-intl';
import { getTranslations } from 'next-intl/server';
import { paletteColor } from '@/lib/utils/palette';

export default async function GlossaryPage() {
  const t = await getTranslations();
  const terms = t.raw('glossary.terms') as Array<{ term: string; desc: string }>;

  return (
    <div className="py-10">
      <h1 className="text-2xl font-bold">{t('glossary.title')}</h1>
      <p className="mt-2 text-slate-600 dark:text-slate-300">{t('glossary.intro')}</p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {terms.map((it, idx) => (
          <div
            key={idx}
            className="glass rounded-xl p-5 border"
            style={{ backgroundColor: paletteColor(idx) }}
          >
            <div className="font-semibold">{it.term}</div>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{it.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
