import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { getLocale } from 'next-intl/server';
import { Oswald, Raleway, Noto_Sans_Hebrew } from 'next/font/google';
import './globals.css';

const oswald = Oswald({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-oswald',
  display: 'swap',
});

const raleway = Raleway({
  subsets: ['latin'],
  weight: ['400', '600', '700', '800'],
  variable: '--font-raleway',
  display: 'swap',
});

const notoSansHebrew = Noto_Sans_Hebrew({
  subsets: ['hebrew'],
  weight: ['300'],
  variable: '--font-noto-hebrew',
  display: 'swap',
});

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const locale = await getLocale();
  const messages = await getMessages();
  const isRtl = locale === 'he';

  return (
    <html lang={locale} dir={isRtl ? 'rtl' : 'ltr'}>
      <head>
        <link rel="icon" href="/Inclusify.png" />
        <meta name="description" content="Inclusive Language Analyzer for academic texts" />
        <meta name="color-scheme" content="light dark" />
      </head>
      <body className={`${oswald.variable} ${raleway.variable} ${notoSansHebrew.variable} min-h-dvh bg-hero-gradient`}>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
