import { getTranslations, getLocale } from 'next-intl/server';
import Link from 'next/link';

export default async function HomePage() {
  const t = await getTranslations();
  const locale = await getLocale();

  const features = [
    {
      key: 'smartDetection',
      color: '#E5D9F2',
      emoji: '🧠',
    },
    {
      key: 'bilingualSupport',
      color: '#D1E9F6',
      emoji: '🌐',
    },
    {
      key: 'gradedAlerts',
      color: '#FFF8DE',
      emoji: '⚠️',
    },
    {
      key: 'exportableReports',
      color: '#E7FBBE',
      emoji: '📄',
    },
    {
      key: 'educationalResources',
      color: '#FFEAEA',
      emoji: '📖',
    },
    {
      key: 'privacyFirst',
      color: '#F5EFFF',
      emoji: '🔒',
    },
  ];

  const isHebrew = locale === 'he';

  return (
    <div className="py-12 sm:py-16">
      <section className="text-center">
        <div className="mx-auto max-w-3xl">
          <h1
            className={`text-4xl sm:text-5xl ${
              isHebrew ? 'font-light hebrew-hero' : 'font-black'
            } tracking-tight bg-gradient-to-tr from-pride-purple to-pride-pink bg-clip-text text-transparent`}
          >
            {isHebrew ? (
              <>
                <span className="block">{t('home.heroHeadlineTop')}</span>
                <span className="block">{t('home.heroHeadlineBottom')}</span>
              </>
            ) : (
              t('home.heroHeadline')
            )}
          </h1>
          <p className="mt-4 text-lg text-slate-600 dark:text-slate-300">
            {isHebrew ? (
              <>
                <span className="brand-raleway text-pride-purple font-extrabold">INCLUSIFY</span>{' '}
                מאתרת ניסוחים בעייתיים ומציעה לכם נוסח חדש מקצועי ומכבד יותר - בלחיצת כפתור!
              </>
            ) : (
              t('home.heroSub')
            )}
          </p>
          <div className="mt-8 flex items-center justify-center gap-3">
            <Link href={`/${locale}/analyze`} className="btn-primary">
              {t('app.cta')}
            </Link>
            <Link href={`/${locale}/glossary`} className="btn-ghost">
              {t('app.glossary')}
            </Link>
          </div>
        </div>
      </section>

      <section className="mt-16 grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3 sm:gap-7 lg:gap-8">
        {features.map((f, i) => (
          <div
            key={i}
            className="rounded-2xl p-6 sm:p-7 lg:p-8 border shadow-soft-xl"
            style={{ backgroundColor: f.color }}
          >
            <div className="flex items-start gap-4">
              <div className="h-12 w-12 rounded-xl grid place-items-center text-2xl bg-white/70">
                <span role="img" aria-label={f.key}>
                  {f.emoji}
                </span>
              </div>
              <div>
                <h3 className="text-lg sm:text-xl font-extrabold">
                  {t(`home.featuresDetailed.${f.key}.title`)}
                </h3>
                <p className="mt-2 text-slate-700 dark:text-slate-300 text-sm sm:text-base">
                  {t(`home.featuresDetailed.${f.key}.desc`)}
                </p>
              </div>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
