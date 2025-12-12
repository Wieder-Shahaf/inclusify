import { getRequestConfig } from 'next-intl/server';

export const locales = ['en', 'he'] as const;
export type Locale = (typeof locales)[number];

export default getRequestConfig(async ({ locale }) => {
  // Middleware already validates the locale, so we can safely use it
  // Default to 'en' if somehow an invalid locale gets through
  const validLocale = (locales.includes(locale as Locale) ? locale : 'en') as Locale;

  return {
    locale: validLocale,
    messages: (await import(`../messages/${validLocale}.json`)).default,
  };
});
